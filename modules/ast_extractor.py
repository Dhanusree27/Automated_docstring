"""
AST Metadata Extraction Module.

Performs deep analysis of Python files using the ast module.
Extracts class/function definitions, arguments, type hints, return types, exceptions.
Detects documentation debt (missing docstrings, PEP 257 compliance issues).
"""
import ast
import inspect
from typing import Dict, List, Any, Optional, Tuple, Set


class ASTExtractor:
    """Extract metadata from Python source code using AST analysis."""

    def __init__(self, source_code: str, file_path: str = ""):
        """
        Initialize the AST extractor.

        Args:
            source_code: Python source code as a string.
            file_path: Optional file path for context.
        """
        self.source_code = source_code
        self.file_path = file_path
        self.tree = None
        self.classes: Dict[str, Dict[str, Any]] = {}
        self.functions: Dict[str, Dict[str, Any]] = {}
        self.parse_tree()

    def parse_tree(self) -> None:
        """
        Parse the source code into an AST tree.

        Raises:
            SyntaxError: If the source code is invalid Python.
        """
        try:
            self.tree = ast.parse(self.source_code)
        except SyntaxError as e:
            raise SyntaxError(f"Failed to parse {self.file_path}: {str(e)}")

    def extract_all_metadata(self) -> Dict[str, Any]:
        """
        Extract all metadata from the source code.

        Returns:
            Dictionary containing classes, functions, and documentation debt info.
        """
        self._extract_classes()
        self._extract_functions()
        debt = self._detect_documentation_debt()

        return {
            "file_path": self.file_path,
            "classes": self.classes,
            "functions": self.functions,
            "documentation_debt": debt,
            "summary": self._generate_summary()
        }

    def _extract_classes(self) -> None:
        """Extract all class definitions and their metadata."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                self.classes[node.name] = {
                    "docstring": ast.get_docstring(node),
                    "methods": {},
                    "attributes": [],
                    "bases": [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
                    "line_number": node.lineno,
                    "is_private": node.name.startswith("_")
                }

                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = self._extract_function_info(item)
                        self.classes[node.name]["methods"][item.name] = method_info

                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                self.classes[node.name]["attributes"].append({
                                    "name": target.id,
                                    "line_number": item.lineno
                                })

    def _extract_functions(self) -> None:
        """Extract all function definitions at module level."""
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef) and not self._is_method(node):
                self.functions[node.name] = self._extract_function_info(node)

    def _extract_function_info(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """
        Extract detailed information about a function.

        Args:
            node: ast.FunctionDef node.

        Returns:
            Dictionary with function metadata.
        """
        args = self._extract_arguments(node.args)
        return_type = self._extract_return_type(node)
        exceptions = self._extract_exceptions(node)

        return {
            "docstring": ast.get_docstring(node),
            "arguments": args,
            "return_type": return_type,
            "exceptions": exceptions,
            "line_number": node.lineno,
            "is_private": node.name.startswith("_"),
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "decorators": [dec.id if isinstance(dec, ast.Name) else str(dec) for dec in node.decorator_list]
        }

    def _extract_arguments(self, args: ast.arguments) -> List[Dict[str, Any]]:
        """
        Extract function arguments with defaults and type hints.

        Args:
            args: ast.arguments node.

        Returns:
            List of argument dictionaries.
        """
        arguments = []
        num_defaults = len(args.defaults)
        num_args = len(args.args)
        defaults = [None] * (num_args - num_defaults) + args.defaults

        for i, arg in enumerate(args.args):
            arg_info = {
                "name": arg.arg,
                "type_hint": self._get_annotation_string(arg.annotation),
                "default": self._get_default_string(defaults[i]) if defaults[i] else None
            }
            arguments.append(arg_info)

        # Handle keyword-only arguments
        for arg in args.kwonlyargs:
            arg_info = {
                "name": arg.arg,
                "type_hint": self._get_annotation_string(arg.annotation),
                "default": "keyword-only"
            }
            arguments.append(arg_info)

        return arguments

    def _extract_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """
        Extract return type hint from a function.

        Args:
            node: ast.FunctionDef node.

        Returns:
            Return type as a string or None.
        """
        if node.returns:
            return self._get_annotation_string(node.returns)
        return None

    def _extract_exceptions(self, node: ast.FunctionDef) -> List[str]:
        """
        Extract raised exceptions from a function.

        Args:
            node: ast.FunctionDef node.

        Returns:
            List of exception names.
        """
        exceptions: Set[str] = set()
        for item in ast.walk(node):
            if isinstance(item, ast.Raise):
                if item.exc:
                    if isinstance(item.exc, ast.Call):
                        if isinstance(item.exc.func, ast.Name):
                            exceptions.add(item.exc.func.id)
                    elif isinstance(item.exc, ast.Name):
                        exceptions.add(item.exc.id)
        return list(exceptions)

    def _get_annotation_string(self, annotation: Optional[ast.expr]) -> Optional[str]:
        """Convert AST annotation to string."""
        if annotation is None:
            return None
        try:
            return ast.unparse(annotation)
        except Exception:
            return str(annotation)

    def _get_default_string(self, default: Optional[ast.expr]) -> Optional[str]:
        """Convert AST default value to string."""
        if default is None:
            return None
        try:
            return ast.unparse(default)
        except Exception:
            return str(default)

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if a function is a method (inside a class)."""
        for parent in ast.walk(self.tree):
            if isinstance(parent, ast.ClassDef):
                for item in parent.body:
                    if item == node:
                        return True
        return False

    def _detect_documentation_debt(self) -> Dict[str, Any]:
        """
        Detect missing docstrings and PEP 257 violations.

        Returns:
            Dictionary with documentation debt metrics.
        """
        debt = {
            "missing_class_docstrings": [],
            "missing_method_docstrings": [],
            "missing_function_docstrings": [],
            "pep257_violations": []
        }

        for class_name, class_info in self.classes.items():
            if not class_info["is_private"] and not class_info["docstring"]:
                debt["missing_class_docstrings"].append(class_name)

            for method_name, method_info in class_info["methods"].items():
                is_private = method_name.startswith("_")
                is_special = method_name.startswith("__") and method_name.endswith("__")
                if not is_private and not method_info["docstring"]:
                    debt["missing_method_docstrings"].append(f"{class_name}.{method_name}")

        for func_name, func_info in self.functions.items():
            if not func_info["is_private"] and not func_info["docstring"]:
                debt["missing_function_docstrings"].append(func_name)

        return debt

    def _generate_summary(self) -> Dict[str, int]:
        """Generate a summary of extracted metadata."""
        return {
            "total_classes": len(self.classes),
            "total_functions": len(self.functions),
            "total_methods": sum(len(c["methods"]) for c in self.classes.values()),
            "undocumented_classes": len([c for c in self.classes.values() if not c["docstring"]]),
            "undocumented_functions": len([f for f in self.functions.values() if not f["docstring"]]),
            "documented_classes": len([c for c in self.classes.values() if c["docstring"]]),
            "documented_functions": len([f for f in self.functions.values() if f["docstring"]])
        }

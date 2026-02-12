"""
Docstring Fixer Module.

Automatically corrects minor formatting errors in docstrings.
"""
import re
from typing import Dict, List, Tuple, Optional


class DocstringFixer:
    """Fixes common docstring formatting errors."""

    def __init__(self):
        """Initialize the docstring fixer."""
        self.fixes_applied = []

    def fix_file(self, source_code: str) -> Tuple[str, Dict[str, List[str]]]:
        """
        Fix all docstrings in a Python file.

        Args:
            source_code: The source code to fix.

        Returns:
            Tuple of (fixed_code, fixes_by_element).
        """
        import ast

        self.fixes_applied = []

        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return source_code, {}

        lines = source_code.split("\n")
        fixes_by_element = {}

        # Fix module docstring
        module_docstring = ast.get_docstring(tree)
        if module_docstring:
            fixed_docstring, changes = self._fix_docstring(module_docstring)
            if changes:
                fixes_by_element["<module>"] = changes
                lines = self._replace_docstring_in_lines(lines, module_docstring, fixed_docstring)

        # Fix class and function docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    fixed_docstring, changes = self._fix_docstring(docstring)
                    if changes:
                        fixes_by_element[node.name] = changes
                        lines = self._replace_docstring_in_lines(lines, docstring, fixed_docstring)

        return "\n".join(lines), fixes_by_element

    def _fix_docstring(self, docstring: str) -> Tuple[str, List[str]]:
        """
        Fix a single docstring.

        Args:
            docstring: The docstring to fix.

        Returns:
            Tuple of (fixed_docstring, list_of_changes).
        """
        changes = []
        lines = docstring.split("\n")

        # 1. Fix capitalization of first character
        if lines and lines[0]:
            first_line = lines[0].strip()
            if first_line and not first_line[0].isupper() and first_line[0].isalpha():
                lines[0] = lines[0].replace(lines[0], first_line[0].upper() + first_line[1:], 1)
                changes.append("Fixed: Capitalized first character")

        # 2. Add missing period
        if lines:
            first_line = lines[0].strip()
            if first_line and not first_line.endswith((".", "?", "!")):
                lines[0] = lines[0].rstrip() + "."
                changes.append("Fixed: Added period to end of summary")

        # 3. Ensure blank line after summary
        if len(lines) > 1:
            summary = lines[0].strip()
            next_line = lines[1].strip() if len(lines) > 1 else ""

            if summary and next_line and next_line not in ["Args:", "Returns:", "Raises:", "Examples:", "Note:", "Attributes:"]:
                lines.insert(1, "")
                changes.append("Fixed: Added blank line after summary")

        # 4. Fix spacing in sections
        for i, line in enumerate(lines):
            # Add colon to section headers if missing
            if any(line.strip().startswith(section) for section in ["Args", "Returns", "Raises", "Examples", "Note", "Attributes"]):
                if not line.rstrip().endswith(":"):
                    lines[i] = line.rstrip() + ":"
                    changes.append(f"Fixed: Added colon to section header '{line.strip()}'")

        # 5. Fix indentation
        fixed_lines = []
        for i, line in enumerate(lines):
            if i > 0 and line.startswith(" "):
                # Ensure consistent 4-space indentation for continuation
                stripped = line.lstrip()
                indent_level = (len(line) - len(stripped)) // 4
                fixed_lines.append("    " * indent_level + stripped)
                if line != fixed_lines[-1]:
                    changes.append("Fixed: Corrected indentation")
            else:
                fixed_lines.append(line)

        fixed_docstring = "\n".join(fixed_lines)
        return fixed_docstring, changes

    def _replace_docstring_in_lines(
        self,
        lines: List[str],
        old_docstring: str,
        new_docstring: str
    ) -> List[str]:
        """Replace a docstring in the lines of code."""
        old_lines = old_docstring.split("\n")
        new_lines = new_docstring.split("\n")

        result = lines[:]
        old_start = None

        # Find the starting line of the docstring
        for i, line in enumerate(result):
            if old_lines[0] in line:
                old_start = i
                break

        if old_start is not None and len(old_lines) <= len(result) - old_start:
            # Replace the old docstring with the new one
            result[old_start:old_start + len(old_lines)] = new_lines

        return result

    def fix_common_errors(self, docstring: str) -> Tuple[str, List[str]]:
        """
        Fix common docstring errors.

        Args:
            docstring: The docstring to fix.

        Returns:
            Tuple of (fixed_docstring, list_of_fixes).
        """
        fixes = []
        fixed = docstring

        # Fix: Multiple spaces
        if "  " in fixed:
            fixed = re.sub(r" {2,}", " ", fixed)
            fixes.append("Removed multiple spaces")

        # Fix: Extra blank lines
        fixed = re.sub(r"\n{3,}", "\n\n", fixed)
        if docstring != fixed:
            fixes.append("Removed extra blank lines")

        # Fix: Trailing whitespace
        fixed = "\n".join(line.rstrip() for line in fixed.split("\n"))
        if docstring != fixed:
            fixes.append("Removed trailing whitespace")

        return fixed, fixes

    def validate_and_fix(self, docstring: str) -> Dict[str, any]:
        """
        Validate and optionally fix a docstring.

        Args:
            docstring: The docstring to validate and fix.

        Returns:
            Dictionary with validation and fix information.
        """
        fixed, fixes = self._fix_docstring(docstring)
        common_fixes = self.fix_common_errors(fixed)

        all_fixes = fixes + common_fixes[1]

        return {
            "original": docstring,
            "fixed": common_fixes[0],
            "fixes_applied": all_fixes,
            "needs_fixing": len(all_fixes) > 0,
            "num_fixes": len(all_fixes)
        }

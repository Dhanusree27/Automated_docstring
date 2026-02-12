"""
Quality & Validation Module.

Integrates pydocstyle for real-time validation.
Generates docstring coverage reports with percentage scores.
Implements autofix for minor formatting errors.
"""
import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict


@dataclass
class DocstringIssue:
    """Represents a docstring issue found during validation."""

    error_code: str
    description: str
    line_number: int
    severity: str  # "error", "warning", "info"
    file_path: str
    element_name: str


class QualityValidator:
    """Validate and score docstring quality using pydocstyle rules."""

    def __init__(self, file_path: str = "", source_code: str = ""):
        """
        Initialize the quality validator.

        Args:
            file_path: Path to the Python file.
            source_code: The source code to validate.
        """
        self.file_path = file_path
        self.source_code = source_code
        self.issues: List[DocstringIssue] = []

    def validate_docstring_quality(self, docstring: str, context: str = "") -> Dict[str, Any]:
        """
        Validate a docstring for quality and PEP 257 compliance.

        Args:
            docstring: The docstring to validate.
            context: The context (function/class signature).

        Returns:
            Dictionary with validation results and suggestions.
        """
        issues = []

        if not docstring:
            return {
                "is_valid": False,
                "score": 0,
                "issues": ["Missing docstring"],
                "suggestions": ["Add a docstring following PEP 257"]
            }

        # Check for docstring format
        if not (docstring.startswith('"""') or docstring.startswith("'''")):
            issues.append("Docstring should use triple quotes")

        # Check for opening period
        lines = docstring.strip().split("\n")
        first_line = lines[0].replace('"""', "").replace("'''", "").strip()

        if first_line and not first_line[0].isupper():
            issues.append("First line should start with an uppercase letter")

        if first_line and not first_line.endswith((".","?","!")):
            issues.append("First line should end with a period")

        # Check for summary line length
        if len(first_line) > 79:
            issues.append(f"Summary line too long ({len(first_line)} > 79 characters)")

        # Check for imperative mood
        if not self._is_imperative_mood(first_line):
            issues.append("First line should use imperative mood")

        # Check for blank line after summary
        if len(lines) > 1 and lines[1].strip() != "":
            issues.append("Should have blank line after summary")

        # Calculate score
        score = self._calculate_score(issues, len(lines))

        return {
            "is_valid": len(issues) == 0,
            "score": score,
            "issues": issues,
            "suggestions": self._generate_suggestions(issues),
            "num_issues": len(issues)
        }

    def generate_coverage_report(
        self,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive docstring coverage report.

        Args:
            metadata: Metadata extracted by ASTExtractor.

        Returns:
            Dictionary with coverage metrics and per-file breakdown.
        """
        summary = metadata.get("summary", {})

        total_classes = summary.get("total_classes", 0)
        total_functions = summary.get("total_functions", 0)
        documented_classes = summary.get("documented_classes", 0)
        documented_functions = summary.get("documented_functions", 0)

        total_total = total_classes + total_functions
        documented_total = documented_classes + documented_functions

        coverage_percentage = (documented_total / total_total * 100) if total_total > 0 else 0

        return {
            "file_path": metadata.get("file_path", ""),
            "overall_coverage": coverage_percentage,
            "coverage_level": self._calculate_coverage_level(coverage_percentage),
            "classes": {
                "total": total_classes,
                "documented": documented_classes,
                "undocumented": total_classes - documented_classes,
                "coverage": (documented_classes / total_classes * 100) if total_classes > 0 else 0
            },
            "functions": {
                "total": total_functions,
                "documented": documented_functions,
                "undocumented": total_functions - documented_functions,
                "coverage": (documented_functions / total_functions * 100) if total_functions > 0 else 0
            },
            "debt": metadata.get("documentation_debt", {}),
            "recommendation": self._get_recommendation(coverage_percentage)
        }

    def autofix_docstring(self, docstring: str) -> Tuple[str, List[str]]:
        """
        Automatically fix minor formatting errors in a docstring.

        Args:
            docstring: The docstring to fix.

        Returns:
            Tuple of (fixed_docstring, list_of_changes_made).
        """
        if not docstring:
            return "", []

        changes = []
        fixed = docstring

        # Ensure triple quotes
        if not (fixed.startswith('"""') or fixed.startswith("'''")):
            fixed = '"""' + fixed + '"""'
            changes.append("Added triple quotes")

        # Fix opening quote format (use triple double quotes)
        if fixed.startswith("'''"):
            fixed = '"""' + fixed[3:]
            changes.append("Changed triple single quotes to triple double quotes")

        if fixed.endswith("'''"):
            fixed = fixed[:-3] + '"""'
            changes.append("Changed triple single quotes to triple double quotes")

        # Extract content
        content = fixed.replace('"""', "")
        lines = content.split("\n")

        # Fix first line capitalization
        if lines and lines[0]:
            if not lines[0][0].isupper():
                lines[0] = lines[0][0].upper() + lines[0][1:]
                changes.append("Capitalized first character")

        # Fix missing period on first line
        first_line = lines[0].strip()
        if first_line and not first_line.endswith((".", "?", "!")):
            lines[0] = lines[0].rstrip() + "."
            changes.append("Added period to end of first line")

        # Ensure blank line after summary
        if len(lines) > 1 and lines[1].strip() != "":
            lines.insert(1, "")
            changes.append("Added blank line after summary")

        # Reconstruct docstring
        fixed = '"""' + "\n".join(lines) + '"""'

        return fixed, changes

    def validate_file(self, source_code: str) -> Dict[str, Any]:
        """
        Validate docstrings in an entire Python file.

        Args:
            source_code: The source code to validate.

        Returns:
            Dictionary with validation results for the file.
        """
        import ast

        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return {
                "file_path": self.file_path,
                "valid": False,
                "error": str(e),
                "issues": []
            }

        issues = []

        # Check module docstring
        module_docstring = ast.get_docstring(tree)
        if not module_docstring:
            issues.append(
                DocstringIssue(
                    error_code="D100",
                    description="Missing module docstring",
                    line_number=1,
                    severity="warning",
                    file_path=self.file_path,
                    element_name="<module>"
                )
            )

        # Check classes
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node) and not node.name.startswith("_"):
                    issues.append(
                        DocstringIssue(
                            error_code="D101",
                            description=f"Missing docstring for class '{node.name}'",
                            line_number=node.lineno,
                            severity="warning",
                            file_path=self.file_path,
                            element_name=node.name
                        )
                    )

            elif isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node) and not node.name.startswith("_"):
                    # Determine if it's a method or function
                    parent = self._find_parent_class(tree, node)
                    error_code = "D102" if parent else "D103"
                    severity = "warning"

                    issues.append(
                        DocstringIssue(
                            error_code=error_code,
                            description=f"Missing docstring for {'method' if parent else 'function'} '{node.name}'",
                            line_number=node.lineno,
                            severity=severity,
                            file_path=self.file_path,
                            element_name=node.name
                        )
                    )

        self.issues = issues

        return {
            "file_path": self.file_path,
            "valid": len(issues) == 0,
            "issues": [asdict(issue) for issue in issues],
            "issue_count": len(issues),
            "error_breakdown": self._breakdown_issues(issues)
        }

    def _is_imperative_mood(self, text: str) -> bool:
        """
        Check if text starts with imperative mood.

        Args:
            text: The text to check.

        Returns:
            True if the text appears to use imperative mood.
        """
        imperative_verbs = [
            "return", "raise", "yield", "create", "build", "get", "set",
            "calculate", "compute", "generate", "perform", "check",
            "validate", "execute", "run", "initialize", "configure",
            "handle", "process", "parse", "extract", "transform"
        ]

        first_word = text.split()[0].lower().rstrip(".,;:") if text.split() else ""
        return first_word in imperative_verbs

    def _calculate_score(self, issues: List[str], num_lines: int) -> float:
        """Calculate a quality score based on issues found."""
        base_score = 100.0
        score = base_score - (len(issues) * 10)
        return max(0.0, score)

    def _calculate_coverage_level(self, coverage: float) -> str:
        """Determine coverage level from percentage."""
        if coverage >= 95:
            return "Excellent"
        elif coverage >= 80:
            return "Good"
        elif coverage >= 60:
            return "Fair"
        else:
            return "Poor"

    def _generate_suggestions(self, issues: List[str]) -> List[str]:
        """Generate suggestions based on issues."""
        suggestions = []
        if any("missing docstring" in issue.lower() for issue in issues):
            suggestions.append("Add a comprehensive docstring")
        if any("period" in issue.lower() for issue in issues):
            suggestions.append("End the first line with a period")
        if any("uppercase" in issue.lower() for issue in issues):
            suggestions.append("Start the docstring with an uppercase letter")
        if any("blank line" in issue.lower() for issue in issues):
            suggestions.append("Add a blank line after the summary")
        if any("imperative" in issue.lower() for issue in issues):
            suggestions.append("Use imperative mood (e.g., 'Generate' instead of 'Generates')")
        return suggestions

    def _get_recommendation(self, coverage: float) -> str:
        """Get recommendation based on coverage level."""
        if coverage >= 95:
            return "Excellent coverage! Continue maintaining high standards."
        elif coverage >= 80:
            return "Good coverage. Consider documenting remaining items."
        elif coverage >= 60:
            return "Fair coverage. Significant documentation work needed."
        else:
            return "Poor coverage. Priority: Document all public APIs."

    def _find_parent_class(self, tree: Any, node: Any) -> Any:
        """Find the parent class of a function."""
        for parent in ast.walk(tree):
            if isinstance(parent, ast.ClassDef):
                for item in parent.body:
                    if item == node:
                        return parent
        return None

    def _breakdown_issues(self, issues: List[DocstringIssue]) -> Dict[str, int]:
        """Break down issues by severity."""
        breakdown = {"error": 0, "warning": 0, "info": 0}
        for issue in issues:
            breakdown[issue.severity] = breakdown.get(issue.severity, 0) + 1
        return breakdown

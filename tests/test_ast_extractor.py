"""Tests for AST Extractor module."""
import pytest
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modules.ast_extractor import ASTExtractor


def test_extract_simple_function():
    """Test extraction of a simple function."""
    code = '''
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''
    extractor = ASTExtractor(code, "test.py")
    metadata = extractor.extract_all_metadata()

    assert "functions" in metadata
    assert "add_numbers" in metadata["functions"]
    func_info = metadata["functions"]["add_numbers"]
    assert func_info["docstring"] == "Add two numbers."
    assert len(func_info["arguments"]) == 2
    assert func_info["return_type"] == "int"


def test_extract_class():
    """Test extraction of a class."""
    code = '''
class Calculator:
    """A simple calculator class."""

    def __init__(self):
        self.value = 0

    def add(self, x: int) -> None:
        """Add x to value."""
        self.value += x
'''
    extractor = ASTExtractor(code, "test.py")
    metadata = extractor.extract_all_metadata()

    assert "classes" in metadata
    assert "Calculator" in metadata["classes"]
    class_info = metadata["classes"]["Calculator"]
    assert class_info["docstring"] == "A simple calculator class."
    assert len(class_info["methods"]) == 2  # __init__ and add


def test_missing_docstrings():
    """Test detection of missing docstrings."""
    code = '''
def func_without_docstring(a, b):
    return a + b

class ClassWithoutDocstring:
    pass
'''
    extractor = ASTExtractor(code, "test.py")
    metadata = extractor.extract_all_metadata()

    debt = metadata["documentation_debt"]
    assert "func_without_docstring" in debt["missing_function_docstrings"]
    assert "ClassWithoutDocstring" in debt["missing_class_docstrings"]


def test_syntax_error():
    """Test handling of syntax errors."""
    code = "def broken function("
    with pytest.raises(SyntaxError):
        ASTExtractor(code, "test.py")

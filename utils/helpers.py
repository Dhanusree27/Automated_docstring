"""
Helper utilities for the Automated Docstring Generator.
"""
import os
from typing import List


def get_python_files(directory: str) -> List[str]:
    """
    Recursively collect all Python files from a directory.

    Args:
        directory: Path to the directory to scan.

    Returns:
        List of absolute paths to Python files.
    """
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def read_file(file_path: str) -> str:
    """
    Read the contents of a file.

    Args:
        file_path: Path to the file.

    Returns:
        File contents as a string.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(file_path: str, content: str) -> bool:
    """
    Write content to a file.

    Args:
        file_path: Path to the file.
        content: Content to write.

    Returns:
        True if successful, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {str(e)}")
        return False


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    Format a decimal value as a percentage string.

    Args:
        value: The decimal value.
        decimal_places: Number of decimal places to display.

    Returns:
        Formatted percentage string.
    """
    return f"{value * 100:.{decimal_places}f}%"


def extract_function_signature(source_code: str, function_name: str) -> str:
    """
    Extract a function signature from source code.

    Args:
        source_code: The source code.
        function_name: The function name.

    Returns:
        The function signature or empty string if not found.
    """
    lines = source_code.split("\n")
    for i, line in enumerate(lines):
        if f"def {function_name}" in line:
            signature = line.strip()
            # Handle multi-line signatures
            j = i + 1
            while j < len(lines) and ":" not in signature:
                signature += " " + lines[j].strip()
                j += 1
            return signature
    return ""

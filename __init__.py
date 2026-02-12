"""
Automated Python Docstring Generator

A professional, modular Python docstring generator with:
- Multi-API failover logic (Google Gemini, Groq, OpenAI)
- AST metadata extraction
- Quality validation with pydocstyle
- Advanced Streamlit UI
- CLI wrapper with scan, report, and apply commands
- CI/CD integration (GitHub Actions, pre-commit)
"""

__version__ = "1.0.0"
__author__ = "Senior Full-Stack Engineer"
__license__ = "MIT"

from modules import (
    ASTExtractor,
    SynthesisEngine,
    Provider,
    QualityValidator,
    DocstringFixer,
    ReportGenerator
)

__all__ = [
    "ASTExtractor",
    "SynthesisEngine",
    "Provider",
    "QualityValidator",
    "DocstringFixer",
    "ReportGenerator"
]

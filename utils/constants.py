"""
Constants and configuration for the Automated Docstring Generator.
"""

# Docstring Styles
DOCSTRING_STYLES = {
    "google": "Google Style",
    "numpy": "NumPy Style",
    "rest": "reStructuredText Style"
}

# Default Style
DEFAULT_STYLE = "google"

# Pydocstyle Error Codes
PYDOCSTYLE_ERROR_CODES = {
    "D100": "Missing docstring in public module",
    "D101": "Missing docstring in public class",
    "D102": "Missing docstring in public method",
    "D103": "Missing docstring in public function",
    "D104": "Missing docstring in public package",
    "D105": "Missing docstring in magic method",
    "D200": "One-line docstring should fit on one line",
    "D201": "Blank line after one-line docstring",
    "D202": "No blank lines allowed after function docstring",
    "D203": "1 blank line required before class docstring",
    "D204": "1 blank line required after class docstring",
    "D205": "1 blank line required between description and arguments",
    "D206": "Docstring should end with a newline, not a backslash",
    "D207": "Docstring is under-indented",
    "D208": "Docstring is over-indented",
    "D209": "Multi-line docstring close-quotes should be on a separate line",
    "D210": "No whitespace before ':'",
    "D211": "Blank line before class docstring",
    "D212": "Multi-line docstring summary should start at the first line",
    "D213": "Multi-line docstring summary should start at the second line",
    "D214": "Section is over-indented",
    "D215": "Section underline is over-indented",
    "D216": "Section name should end with a colon",
    "D217": "Section name should be a single line",
    "D218": "Imperative mood should be used for the first line of the docstring",
    "D300": "Use \"\"\"triple double quotes\"\"\"",
    "D301": "Use r\"\"\" if any backslashes in your docstring",
    "D302": "Use \"\"\"triple double quotes\"\"\"",
    "D400": "First line should end with a period",
    "D401": "First line should be in imperative mood",
    "D402": "First line should not be the function signature",
    "D403": "First word of the first line should be properly capitalized",
}

# API Configuration
API_PROVIDERS = {
    "google": {"name": "Google Gemini", "model": "gemini-2.5-flash"},
    "groq": {"name": "Groq", "model": "llama-3.3-70b-versatile"}
}


# Rate Limit and Timeout
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# File Extensions
PYTHON_EXTENSIONS = [".py"]

# Quality Thresholds
COVERAGE_EXCELLENT = 95
COVERAGE_GOOD = 80
COVERAGE_FAIR = 60
COVERAGE_POOR = 0

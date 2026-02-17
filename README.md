# 📝 Automated Python Docstring Generator

A professional, modular Python docstring generator with multi-API failover logic, AST analysis, quality validation, and an advanced Streamlit UI. Designed for enterprise-grade documentation management.

## 🎯 Features

### 1. Synthesis Engine (Multi-API Failover)
- **Primary:** Google Gemini (gemini-2.5-flash)
- **Secondary:** Groq (llama-3.3-70b-versatile)
- Automatic failover on rate limits or API errors
- Real-time provider status monitoring
- Robust exception handling

### 2. AST Metadata Extraction (Module 1)
- Deep analysis of Python code using `ast` module
- Extract class/function definitions, arguments, type hints, return types
- Detect exceptions raised in functions
- Identify "Documentation Debt" (missing docstrings, PEP 257 violations)
- Comprehensive code structure analysis

### 3. Quality & Validation (Module 3)
- Integrated `pydocstyle` validation
- Docstring Coverage Reports with percentage scores
- Per-file and project-level metrics
- Autofix functionality for formatting errors
- PEP 257 compliance checking

### 4. Advanced Streamlit UI (Module 6)
- **Dashboard:** Project Health summary with compliance charts
- **Code Reviewer:** Side-by-side diff view with Accept/Reject buttons
- **Generator:** Real-time AI docstring generation
- **Reports:** JSON, Markdown, and HTML report export
- **Sidebar:** Configuration for styles and API key management

### 5. CLI & Pipeline (Modules 4 & 5)
- Command-line interface with `scan`, `report`, and `apply` commands
- Pre-commit hooks configuration
- GitHub Actions CI/CD workflow for automated checking
- Coverage threshold enforcement

## 📁 Project Structure

```
automated_docstring/
├── app.py                      # Main Streamlit application
├── cli.py                      # CLI wrapper with commands
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── modules/                    # Core modules
│   ├── __init__.py
│   ├── ast_extractor.py       # Module 1: AST analysis
│   ├── synthesis_engine.py    # Multi-API failover logic
│   ├── quality_validator.py   # Module 3: Validation
│   ├── docstring_fixer.py     # Auto-fix formatting
│   └── report_generator.py    # Report generation
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── constants.py           # Configuration constants
│   └── helpers.py             # Helper functions
│
├── .github/workflows/          # CI/CD integration
│   └── docstring-check.yml    # GitHub Actions workflow
│
├── .pre-commit-config.yaml    # Pre-commit hooks config
│
└── tests/                      # Test suite (optional)
    └── __init__.py
```

## 🚀 Quick Start

### Installation

1. Clone or download the project:
```bash
cd automated_docstring
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file in the project root
GOOGLE_API_KEY=your-google-api-key
GROQ_API_KEY=your-groq-api-key
```

### Running the Streamlit UI

```bash
streamlit run app.py
```

The UI will open at `http://localhost:8501` with:
- 📊 Dashboard for project health overview
- 🔍 Code Reviewer for docstring inspection
- 🚀 Generator for creating new docstrings
- 📄 Reports in JSON, Markdown, or HTML

### Using the CLI

#### Scan for Documentation Issues

```bash
python cli.py scan src/
python cli.py scan src/ --output scan_results.json
```

#### Generate Coverage Report

```bash
python cli.py report src/ --format json --output report.json
python cli.py report src/ --format markdown --output report.md
python cli.py report src/ --format html --output report.html
```

#### Apply Docstring Generation

```bash
python cli.py apply src/ --style google
python cli.py apply src/ --style google --autofix --dry-run
```

## 📚 Docstring Styles Supported

### Google Style
```python
"""Brief description.

Extended description if needed.

Args:
    param1 (str): Description of param1.
    param2 (int): Description of param2.

Returns:
    bool: Description of return value.

Raises:
    ValueError: Description of when this is raised.
"""
```

### NumPy Style
```python
"""Brief description.

Extended description if needed.

Parameters
----------
param1 : str
    Description of param1.
param2 : int
    Description of param2.

Returns
-------
bool
    Description of return value.

Raises
------
ValueError
    Description of when this is raised.
"""
```

### reStructuredText Style
```python
"""Brief description.

Extended description if needed.

:param param1: Description of param1.
:type param1: str
:param param2: Description of param2.
:type param2: int
:return: Description of return value.
:rtype: bool
:raises ValueError: Description of when this is raised.
"""
```

## 🔄 Failover Logic Example

```python
from modules import SynthesisEngine

engine = SynthesisEngine()

# Automatically handles failover
result = engine.generate_docstring(
    function_signature="def process_data(data: list) -> dict:",
    code_context="# Implementation here",
    docstring_style="google"
)

if result["success"]:
    print(f"✅ Generated with {result['provider']}")
    print(result["docstring"])
else:
    print(f"❌ {result['error']}")
```

## 📊 Coverage Report Example

```bash
python cli.py report src/ --format markdown
```

Output:
```markdown
# Docstring Coverage Report

**Overall Coverage:** 87.5%
**Compliance Status:** ✅ Good

## File Details
| File | Coverage | Classes | Functions | Status |
|------|----------|---------|-----------|--------|
| src/main.py | 92.3% | 5 | 8 | ✓ |
| src/utils.py | 78.0% | 2 | 6 | ⚠ |

## Recommendations
- Target: Increase coverage to 95% for excellence.
- Use the CLI tool to automatically generate docstrings.
```

## 🔧 Configuration

### API Provider Priority
Configured in `utils/constants.py`:
```python
API_PROVIDERS = {
    "google": {"name": "Google Gemini", "model": "gemini-2.5-flash"},
    "groq": {"name": "Groq", "model": "llama-3.3-70b-versatile"}
}
```

### Coverage Thresholds
```python
COVERAGE_EXCELLENT = 95  # Green
COVERAGE_GOOD = 80       # Blue
COVERAGE_FAIR = 60       # Yellow
COVERAGE_POOR = 0        # Red
```

## 🔐 Pre-commit Integration

Setup pre-commit hooks to validate docstrings automatically:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Configured checks:
- Docstring coverage validation
- PEP 257 compliance (pydocstyle)
- Code formatting (black)
- Linting (flake8)
- Import sorting (isort)

## 🚀 GitHub Actions CI/CD

The workflow `.github/workflows/docstring-check.yml` runs on:
- Push to `main` and `develop` branches
- Pull requests

**Features:**
- Automated docstring coverage scanning
- Coverage threshold enforcement (default: 80%)
- Multi-version Python testing (3.8, 3.9, 3.10, 3.11)
- PR comments with coverage results
- Artifact upload for reports

**Enable on GitHub:**
1. Push the `.github/workflows/docstring-check.yml` file
2. The workflow triggers automatically on push/PR
3. Coverage results appear as PR comments

## 📦 Module Reference

### ASTExtractor
```python
from modules import ASTExtractor

extractor = ASTExtractor(source_code, "file.py")
metadata = extractor.extract_all_metadata()

# Returns: classes, functions, documentation_debt, summary
```

### SynthesisEngine
```python
from modules import SynthesisEngine

engine = SynthesisEngine()
result = engine.generate_docstring(
    function_signature="...",
    code_context="...",
    docstring_style="google"
)

# Returns: docstring, provider, success, error
```

### QualityValidator
```python
from modules import QualityValidator

validator = QualityValidator("file.py")

# Validate single docstring
result = validator.validate_docstring_quality(docstring)

# Generate coverage report
report = validator.generate_coverage_report(metadata)

# Validate entire file
validation = validator.validate_file(source_code)
```

### DocstringFixer
```python
from modules import DocstringFixer

fixer = DocstringFixer()

# Fix single docstring
fixed, changes = fixer._fix_docstring(docstring)

# Fix entire file
fixed_code, fixes_dict = fixer.fix_file(source_code)
```

### ReportGenerator
```python
from modules import ReportGenerator

generator = ReportGenerator()

# Generate comprehensive report
report = generator.generate_project_report(
    project_name="MyProject",
    files_metadata=metadata_list,
    coverage_reports=reports_list
)

# Export in different formats
json_report = generator.generate_json_report(report)
md_report = generator.generate_markdown_report(report)
html_report = generator.generate_html_report(report)
```

## ⚡ Performance Considerations

- **AST Analysis:** O(n) where n = number of nodes in AST
- **API Calls:** Cached where possible, implement rate limiting
- **Large Codebases:** Process files in parallel using multiprocessing
- **Memory:** Stream large files instead of loading entirely

## 🛡️ Error Handling

### API Failures
- Automatic provider failover
- Exponential backoff for rate limits
- Detailed error logging

### File Processing
- Syntax error isolation (doesn't stop scanning)
- Graceful handling of encoding issues
- Permission error handling

## 📝 Testing

Run tests:
```bash
pytest tests/
pytest --cov=modules --cov=utils tests/
```

## 🤝 Contributing

1. Create feature branches
2. Ensure docstrings follow Google style
3. Run pre-commit hooks
4. Submit pull requests

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

For issues and feature requests, please create an issue in the repository.

## 🎓 Learning Resources

- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- [NumPy Documentation Guide](https://numpydoc.readthedocs.io/)
- [AST Module Documentation](https://docs.python.org/3/library/ast.html)

---

**Built with ❤️ for professional Python development**

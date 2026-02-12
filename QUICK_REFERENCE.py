#!/usr/bin/env python3
"""
Quick Reference Guide for Automated Python Docstring Generator

A fast lookup guide for common tasks and commands.
"""

QUICK_REFERENCE = """
╔════════════════════════════════════════════════════════════════════════════╗
║                       QUICK REFERENCE GUIDE                               ║
║          Automated Python Docstring Generator v1.0.0                       ║
╚════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 GETTING STARTED (5 minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install Dependencies
   $ pip install -r requirements.txt

2. Setup API Keys
   $ cp .env.example .env
   # Edit .env with your API keys

3. Test Installation
   $ python examples.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 LAUNCHING THE UI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Start Streamlit Web UI:
   $ streamlit run app.py
   
   Opens at: http://localhost:8501
   
   Features:
   • 📊 Dashboard - Project health overview
   • 🔍 Code Review - Docstring inspection
   • 🚀 Generator - AI docstring creation
   • 📄 Reports - Export results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 CLI COMMANDS CHEAT SHEET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCAN FOR ISSUES
   $ python cli.py scan src/
   $ python cli.py scan src/ --output issues.json

GENERATE REPORTS
   JSON Format:
   $ python cli.py report src/ --format json --output report.json
   
   Markdown Format:
   $ python cli.py report src/ --format markdown --output report.md
   
   HTML Format:
   $ python cli.py report src/ --format html --output report.html

APPLY DOCSTRING GENERATION
   Google Style (default):
   $ python cli.py apply src/ --style google
   
   NumPy Style:
   $ python cli.py apply src/ --style numpy
   
   reStructuredText Style:
   $ python cli.py apply src/ --style rest

OPTIONS & FLAGS
   --dry-run         Show changes without writing
   --autofix         Enable auto-fixing of formatting errors
   --output, -o      Specify output file/directory
   --recursive       Scan directories recursively (default: true)
   --project-name    Set project name for reports

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐍 USING AS PYTHON MODULE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Extract Code Metadata:
   from modules import ASTExtractor
   
   extractor = ASTExtractor(source_code, "file.py")
   metadata = extractor.extract_all_metadata()
   
   # Access results
   classes = metadata['classes']
   functions = metadata['functions']
   debt = metadata['documentation_debt']

Generate Docstring:
   from modules import SynthesisEngine
   
   engine = SynthesisEngine()
   result = engine.generate_docstring(
       function_signature="def my_func():",
       code_context="# my implementation",
       docstring_style="google"
   )
   
   print(result['docstring'])

Validate Docstring Quality:
   from modules import QualityValidator
   
   validator = QualityValidator()
   result = validator.validate_docstring_quality(docstring)
   
   # Get suggestions
   print(result['issues'])
   print(result['suggestions'])

Generate Coverage Report:
   from modules import ReportGenerator
   
   generator = ReportGenerator()
   report = generator.generate_project_report(
       "My Project",
       metadata_list,
       coverage_reports
   )
   
   # Export formats
   json_report = generator.generate_json_report(report)
   md_report = generator.generate_markdown_report(report)
   html_report = generator.generate_html_report(report)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️ CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Environment Variables (.env):
   GOOGLE_API_KEY=...       # Google Gemini API key
   GROQ_API_KEY=...         # Groq API key
   OPENAI_API_KEY=...       # OpenAI API key
   ENVIRONMENT=development  # development/production/testing
   LOG_LEVEL=INFO           # DEBUG/INFO/WARNING/ERROR

Coverage Thresholds (config.py):
   Excellent: >= 95%
   Good:      80-95%
   Fair:      60-80%
   Poor:      < 60%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 GIT & PRE-COMMIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Setup Pre-commit Hooks:
   $ pip install pre-commit
   $ pre-commit install
   $ pre-commit run --all-files

Checks that Run:
   ✓ Docstring coverage validation
   ✓ PEP 257 compliance (pydocstyle)
   ✓ Code formatting (black)
   ✓ Linting (flake8)
   ✓ Import sorting (isort)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 CI/CD (GitHub Actions)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Setup GitHub Actions:
   1. Push .github/workflows/docstring-check.yml to GitHub
   2. Workflow runs automatically on:
      • Push to main/develop
      • Pull requests
   
   Features:
   ✓ Automated docstring scanning
   ✓ Coverage threshold enforcement (80%)
   ✓ PR comments with results
   ✓ Multi-Python version testing

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 DOCSTRING STYLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Google Style (Default):
   \"\"\"Brief description.
   
   Extended description here.
   
   Args:
       param1 (type): Description.
   
   Returns:
       type: Description.
   
   Raises:
       Exception: When this happens.
   \"\"\"

NumPy Style:
   \"\"\"Brief description.
   
   Parameters
   ----------
   param1 : type
       Description.
   
   Returns
   -------
   type
       Description.
   \"\"\"

reStructuredText Style:
   \"\"\"Brief description.
   
   :param param1: Description.
   :type param1: type
   :return: Description.
   :rtype: type
   :raises Exception: When.
   \"\"\"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐛 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"ModuleNotFoundError: No module named 'streamlit'"
   → pip install streamlit

"API key not found" error
   → Check .env file is in project root
   → Ensure keys are set correctly (no quotes)
   → Restart your terminal

"Rate limit error"
   → Automatic failover to next provider
   → Check provider status in UI
   → Wait and retry (limits reset hourly)

"Permission denied" saving reports
   → Check folder permissions
   → Create output directory first

"Syntax error in file"
   → Check Python file syntax
   → Run: python -m py_compile file.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 COVERAGE REPORT INTERPRETATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

% Coverage  Status      Interpretation
━━━━━━━━━━  ━━━━━     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
95-100%     ✅ Excellent  All items documented properly
80-94%      ✓  Good       Most items documented well
60-79%      ⚠  Fair       Significant work needed
0-59%       ❌ Poor       Critical documentation required

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ COMMON WORKFLOWS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Workflow 1: Audit Existing Project
   1. python cli.py scan /path/to/project --output issues.json
   2. python cli.py report /path/to/project --format markdown
   3. Review the report and issues list

Workflow 2: Generate Docstrings for Project
   1. python cli.py scan /path/to/project
   2. python cli.py apply /path/to/project --style google --dry-run
   3. python cli.py apply /path/to/project --style google
   4. python cli.py report /path/to/project --format html

Workflow 3: Interactive Review & Generation
   1. streamlit run app.py
   2. Upload your Python files
   3. Review suggestions in Code Reviewer
   4. Generate docstrings for selected items
   5. Accept/reject and export

Workflow 4: CI/CD Integration
   1. Push .github/workflows/docstring-check.yml
   2. Workflow runs automatically on every PR
   3. View results in PR comments
   4. Download detailed reports from artifacts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 HELPFUL LINKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Documentation:
   • README.md - Full project documentation
   • INSTALLATION.md - Step-by-step installation
   • examples.py - Working code examples

Python Standards:
   • PEP 257 - Docstring Conventions
   • Google Style Guide - Python docstrings
   • NumPy Documentation - NumPy style
   • Sphinx - reStructuredText documentation

APIs:
   • Google Gemini - https://aistudio.google.com
   • Groq API - https://console.groq.com
   • OpenAI API - https://platform.openai.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 SUPPORT & RESOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Need Help?
   1. Check README.md for detailed docs
   2. Review examples.py for usage patterns
   3. Check module docstrings for API details
   4. Review PROJECT_SUMMARY.md for overview

File a Bug or Feature Request:
   1. Create issue in repository
   2. Include error message and reproduction steps
   3. Attach relevant files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VERIFICATION CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After Installation:
   □ Python 3.8+ installed
   □ Dependencies installed: pip install -r requirements.txt
   □ .env file configured with API keys
   □ examples.py runs without errors
   □ Streamlit UI launches: streamlit run app.py
   □ CLI commands work: python cli.py --help

Before Production:
   □ All tests pass: pytest tests/
   □ Pre-commit hooks installed: pre-commit install
   □ No style issues: black, flake8 pass
   □ Type checking passes: mypy check
   □ Coverage report generated and reviewed
   □ GitHub Actions workflow configured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 PRO TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Always use --dry-run before applying changes
   $ python cli.py apply src/ --dry-run

2. Save reports in multiple formats for different audiences
   $ python cli.py report src/ --format {json,markdown,html}

3. Use Streamlit UI for interactive review and acceptance
   $ streamlit run app.py

4. Keep .env out of version control
   Add to .gitignore: .env

5. Use pre-commit hooks to enforce standards automatically
   $ pre-commit install

6. Monitor API provider status in the UI
   Good for understanding API issues

7. Generate reports regularly to track progress
   Run weekly/monthly comprehensive audits

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Version: 1.0.0
Last Updated: February 8, 2026
Status: Production Ready ✅

╚════════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(QUICK_REFERENCE)

"""
Installation and Setup Guide for Automated Python Docstring Generator
"""

"""
INSTALLATION STEPS:

1. Prerequisites
   - Python 3.8 or higher
   - pip (Python package manager)
   - Git (optional, for version control)

2. Clone/Download Project
   $ cd automated_docstring

3. Create Virtual Environment (Recommended)
   $ python -m venv venv
   $ source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install Dependencies
   $ pip install -r requirements.txt

5. Configure API Keys
   a) Copy .env.example to .env:
      $ cp .env.example .env
   
   b) Edit .env and add your API keys:
      GOOGLE_API_KEY=your-key-here
      GROQ_API_KEY=your-key-here
      OPENAI_API_KEY=your-key-here

6. (Optional) Setup Pre-commit Hooks
   $ pre-commit install
   $ pre-commit run --all-files

7. Verify Installation
   $ python examples.py
   
   This runs basic examples to verify everything works.

8. Start Using

   a) Streamlit UI:
      $ streamlit run app.py
      
      Open http://localhost:8501 in your browser
   
   b) Command Line:
      $ python cli.py scan src/
      $ python cli.py report src/ --format json
      $ python cli.py apply src/ --style google

   c) As Python Module:
      from modules import ASTExtractor, SynthesisEngine
      # Use modules in your code


OBTAINING API KEYS:

1. Google Gemini
   - Visit: https://aistudio.google.com/app/apikey
   - Create new API key
   - Copy and paste in .env

2. Groq
   - Visit: https://console.groq.com
   - Sign up and log in
   - Create API key
   - Copy and paste in .env

3. OpenAI
   - Visit: https://platform.openai.com/api-keys
   - Create new API key
   - Copy and paste in .env


TROUBLESHOOTING:

1. "ModuleNotFoundError: No module named 'streamlit'"
   Solution: $ pip install streamlit

2. "API key not found" error
   Solution: Check .env file has correct API keys
   - Ensure .env is in project root
   - Check key format (no quotes usually needed)
   - Restart terminal/app after modifying .env

3. Syntax errors when scanning files
   Solution: Check Python file syntax
   - Run: python -m py_compile file.py
   - Fix any syntax issues

4. Rate limit errors
   Solution: Engine automatically switches providers
   - Check provider status in UI
   - APIs usually reset rate limits hourly
   - Consider using less frequent calls

5. Permission denied when saving reports
   Solution: Check file/folder permissions
   - Ensure write access to output directory
   - Create directory if it doesn't exist


QUICK COMMANDS:

# Scan a directory
python cli.py scan ./src

# Generate JSON report
python cli.py report ./src --format json --output report.json

# Generate Markdown report
python cli.py report ./src --format markdown --output report.md

# Generate HTML report
python cli.py report ./src --format html --output report.html

# Apply docstring generation
python cli.py apply ./src --style google

# Dry run (show what would be applied)
python cli.py apply ./src --style google --dry-run

# Run tests
pytest tests/

# Check code with pre-commit hooks
pre-commit run --all-files

# Start Streamlit UI
streamlit run app.py


CONFIGURATION:

Key configuration files:
- .env              : API keys and environment variables
- config.py         : Application settings
- requirements.txt  : Python dependencies
- .pre-commit-config.yaml : Pre-commit hook settings

Default settings (in config.py):
- Coverage threshold (Good): 80%
- Coverage threshold (Excellent): 95%
- Default docstring style: Google
- API timeout: 30 seconds
- Max retries: 3


PROJECT STRUCTURE:

automated_docstring/
├── app.py                          # Streamlit UI
├── cli.py                          # CLI wrapper
├── config.py                       # Configuration
├── examples.py                     # Usage examples
├── requirements.txt                # Dependencies
├── README.md                       # Full documentation
│
├── modules/
│   ├── ast_extractor.py           # AST analysis
│   ├── synthesis_engine.py        # LLM failover
│   ├── quality_validator.py       # Validation
│   ├── docstring_fixer.py         # Auto-fix
│   └── report_generator.py        # Reports
│
├── utils/
│   ├── constants.py               # Constants
│   └── helpers.py                 # Utilities
│
└── .github/workflows/
    └── docstring-check.yml        # GitHub Actions


NEXT STEPS:

1. Run examples to familiar yourself:
   $ python examples.py

2. Try the Streamlit UI:
   $ streamlit run app.py

3. Scan your first project:
   $ python cli.py scan /path/to/your/project

4. Generate a report:
   $ python cli.py report /path/to/your/project --format html

5. Set up CI/CD with GitHub Actions by pushing to GitHub

6. Configure pre-commit hooks for auto-validation:
   $ pre-commit install


ENVIRONMENT VARIABLES:

GOOGLE_API_KEY       - Google Gemini API key
GROQ_API_KEY        - Groq API key
OPENAI_API_KEY      - OpenAI API key
ENVIRONMENT         - development/production/testing
LOG_LEVEL          - DEBUG/INFO/WARNING/ERROR


PERFORMANCE TIPS:

1. Use --dry-run flag to test changes first:
   $ python cli.py apply . --dry-run

2. Scan large directories incrementally:
   $ python cli.py scan ./src --output detailed_report.json

3. Generate Markdown reports for easier sharing:
   $ python cli.py report . --format markdown

4. Use parallel processing for organizations:
   - Modify config.py ENABLE_PARALLEL_PROCESSING = True

5. Cache API results to reduce costs:
   - Set ENABLE_CACHING = True in config.py


GETTING HELP:

1. Check README.md for detailed documentation
2. Review examples.py for usage patterns
3. Check module docstrings for API reference
4. Run: python cli.py --help
5. Create an issue in the repository

---
Questions? See README.md for complete documentation!
"""

# This file serves as documentation. No executable code.

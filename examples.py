"""
Quick Start Examples for Automated Python Docstring Generator
"""

# ============================================================================
# Example 1: Basic AST Extraction
# ============================================================================

def example_ast_extraction():
    """Demonstrate AST metadata extraction."""
    from modules import ASTExtractor
    
    code_sample = """
def calculate_sum(numbers: list) -> int:
    return sum(numbers)
"""
    
    # Extract metadata
    extractor = ASTExtractor(code_sample, "example.py")
    metadata = extractor.extract_all_metadata()
    
    print("Functions found:", list(metadata['functions'].keys()))
    print("Documentation debt:", metadata['documentation_debt'])
    return metadata


# ============================================================================
# Example 2: Synthesis Engine with Failover
# ============================================================================

def example_synthesis_engine():
    """Demonstrate multi-API failover logic."""
    from modules import SynthesisEngine
    
    engine = SynthesisEngine()
    
    # Check provider status
    print("Provider Status:", engine.get_provider_status())
    
    # Generate docstring (with automatic failover)
    result = engine.generate_docstring(
        function_signature="def process_data(data: list) -> dict:",
        code_context="# Process input data and return results",
        docstring_style="google"
    )
    
    if result["success"]:
        print(f"✅ Generated with {result['provider']}")
        print(f"Docstring:\n{result['docstring']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    return result


# ============================================================================
# Example 3: Quality Validation
# ============================================================================

def example_quality_validation():
    """Demonstrate docstring quality validation."""
    from modules import QualityValidator
    
    validator = QualityValidator()
    
    good_docstring = '''"""
    Calculate the sum of numbers.
    
    Args:
        numbers: List of integers to sum.
    
    Returns:
        The total sum of all numbers.
    """'''
    
    bad_docstring = "return sum"
    
    print("Validating good docstring:")
    good_result = validator.validate_docstring_quality(good_docstring)
    print(f"Score: {good_result['score']}/100")
    print(f"Issues: {good_result['issues']}")
    
    print("\nValidating bad docstring:")
    bad_result = validator.validate_docstring_quality(bad_docstring)
    print(f"Score: {bad_result['score']}/100")
    print(f"Issues: {bad_result['issues']}")
    
    return good_result, bad_result


# ============================================================================
# Example 4: Docstring Autofix
# ============================================================================

def example_docstring_autofix():
    """Demonstrate automatic docstring fixing."""
    from modules import DocstringFixer
    
    fixer = DocstringFixer()
    
    broken_docstring = '''"""
    calculate sum
    
    Args:
        numbers: list of numbers
    
    Returns'''
    
    fixed, changes = fixer._fix_docstring(broken_docstring)
    
    print("Original:")
    print(broken_docstring)
    print("\nFixed:")
    print(fixed)
    print("\nChanges applied:")
    for change in changes:
        print(f"  - {change}")
    
    return fixed


# ============================================================================
# Example 5: Coverage Report Generation
# ============================================================================

def example_coverage_report():
    """Generate a coverage report from metadata."""
    from modules import ASTExtractor, QualityValidator, ReportGenerator
    
    code_sample = """
def function1():
    pass

def function2():
    pass

class MyClass:
    def method1(self):
        pass
"""
    
    # Extract and validate
    extractor = ASTExtractor(code_sample, "example.py")
    metadata = extractor.extract_all_metadata()
    
    validator = QualityValidator()
    coverage_report = validator.generate_coverage_report(metadata)
    
    # Generate project report
    generator = ReportGenerator()
    project_report = generator.generate_project_report(
        "Example Project",
        [metadata],
        [coverage_report]
    )
    
    print(f"Overall Coverage: {project_report['summary']['overall_coverage']:.1f}%")
    print(f"Compliance: {project_report['summary']['compliance_status']}")
    
    # Export as markdown
    md_report = generator.generate_markdown_report(project_report)
    print("\nMarkdown Report Sample:")
    print(md_report[:500] + "...")
    
    return project_report


# ============================================================================
# Example 6: CLI Usage
# ============================================================================

def example_cli_usage():
    """Show CLI command examples."""
    examples = """
# Scan for documentation issues
python cli.py scan src/

# Generate coverage report
python cli.py report src/ --format json --output report.json
python cli.py report src/ --format markdown --output report.md
python cli.py report src/ --format html --output report.html

# Apply docstring generation
python cli.py apply src/ --style google
python cli.py apply src/ --style google --dry-run --autofix
"""
    print(examples)


# ============================================================================
# Example 7: Using QualityValidator on Entire File
# ============================================================================

def example_file_validation():
    """Validate entire Python file for docstring compliance."""
    from modules import QualityValidator
    
    code_sample = """'''Module docstring.'''

def function_without_docstring():
    return 42

def documented_function():
    '''This function is documented.'''
    return True
"""
    
    validator = QualityValidator("example.py")
    validation = validator.validate_file(code_sample)
    
    print(f"File valid: {validation['valid']}")
    print(f"Issues found: {validation['issue_count']}")
    for issue in validation['issues'][:3]:
        print(f"  - [{issue['error_code']}] {issue['description']}")
    
    return validation


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("AUTOMATED PYTHON DOCSTRING GENERATOR - QUICK START EXAMPLES")
    print("=" * 70)
    
    print("\n📚 Example 1: AST Extraction")
    print("-" * 70)
    try:
        example_ast_extraction()
    except Exception as e:
        print(f"Note: {e}")
    
    print("\n🔄 Example 2: Synthesis Engine (Requires API Keys)")
    print("-" * 70)
    print("Note: Set GOOGLE_API_KEY, GROQ_API_KEY, OPENAI_API_KEY")
    # example_synthesis_engine()  # Uncomment with API keys
    
    print("\n✅ Example 3: Quality Validation")
    print("-" * 70)
    example_quality_validation()
    
    print("\n🔧 Example 4: Docstring Autofix")
    print("-" * 70)
    example_docstring_autofix()
    
    print("\n📊 Example 5: Coverage Report")
    print("-" * 70)
    example_coverage_report()
    
    print("\n⚙️ Example 6: CLI Commands")
    print("-" * 70)
    example_cli_usage()
    
    print("\n🎯 Example 7: File Validation")
    print("-" * 70)
    example_file_validation()
    
    print("\n" + "=" * 70)
    print("For more information, see README.md")
    print("=" * 70)

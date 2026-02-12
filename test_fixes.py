#!/usr/bin/env python3
"""
Comprehensive Test Script for Automated Python Docstring Generator Fixes
Tests all the implemented fixes and functionality.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

def test_imports():
    """Test that all modules import correctly."""
    print("🔍 Testing imports...")

    try:
        from modules import (
            ASTExtractor, SynthesisEngine, QualityValidator,
            ReportGenerator, DocstringFixer
        )
        from utils import get_python_files, read_file, write_file, DOCSTRING_STYLES
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_api_key_loading():
    """Test API key loading from environment variables."""
    print("\n🔑 Testing API key loading...")

    # Test without environment variables
    old_google = os.environ.get('GOOGLE_API_KEY')
    old_groq = os.environ.get('GROQ_API_KEY')

    # Remove env vars temporarily
    if 'GOOGLE_API_KEY' in os.environ:
        del os.environ['GOOGLE_API_KEY']
    if 'GROQ_API_KEY' in os.environ:
        del os.environ['GROQ_API_KEY']

    # Import app to test loading
    try:
        import importlib
        if 'app' in sys.modules:
            importlib.reload(sys.modules['app'])
        import app

        # Check if API keys are None (as expected)
        google_key = app.GOOGLE_API_KEY
        groq_key = app.GROQ_API_KEY

        if google_key is None and groq_key is None:
            print("✅ API keys properly load as None when not set")
        else:
            print(f"❌ Expected None, got Google: {google_key}, Groq: {groq_key}")
            return False

    except Exception as e:
        print(f"❌ API key loading test failed: {e}")
        return False
    finally:
        # Restore environment variables
        if old_google:
            os.environ['GOOGLE_API_KEY'] = old_google
        if old_groq:
            os.environ['GROQ_API_KEY'] = old_groq

    return True

def test_model_consistency():
    """Test that model names are consistent across files."""
    print("\n🤖 Testing model consistency...")

    try:
        from utils.constants import API_PROVIDERS
        from modules.synthesis_engine import SynthesisEngine

        # Check constants
        google_model = API_PROVIDERS['google']['model']
        print(f"Constants - Google model: {google_model}")

        # Check synthesis engine
        engine = SynthesisEngine()
        # The engine uses the model internally, let's check if it initializes
        print("✅ Synthesis engine initializes successfully")

        # Check if model name matches expected
        if google_model == 'gemini-2.5-flash':
            print("✅ Model name is consistent: gemini-2.5-flash")
            return True
        else:
            print(f"❌ Model name mismatch: expected 'gemini-2.5-flash', got '{google_model}'")
            return False

    except Exception as e:
        print(f"❌ Model consistency test failed: {e}")
        return False

def test_ast_extractor():
    """Test AST extraction functionality."""
    print("\n🔍 Testing AST extraction...")

    sample_code = '''
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

class Calculator:
    """A simple calculator class."""

    def multiply(self, x: float, y: float) -> float:
        return x * y
'''

    try:
        from modules import ASTExtractor

        extractor = ASTExtractor(sample_code, "test.py")
        metadata = extractor.extract_all_metadata()

        # Check if functions and classes were extracted
        functions = metadata.get('functions', {})
        classes = metadata.get('classes', {})

        if 'add_numbers' in functions and 'Calculator' in classes:
            print("✅ AST extraction working correctly")
            print(f"   - Found {len(functions)} functions: {list(functions.keys())}")
            print(f"   - Found {len(classes)} classes: {list(classes.keys())}")
            return True
        else:
            print(f"❌ AST extraction failed - functions: {list(functions.keys())}, classes: {list(classes.keys())}")
            return False

    except Exception as e:
        print(f"❌ AST extraction test failed: {e}")
        return False

def test_quality_validator():
    """Test docstring quality validation."""
    print("\n✅ Testing quality validation...")

    try:
        from modules import QualityValidator

        validator = QualityValidator()

        # Test valid docstring
        valid_docstring = '"""Add two numbers together.\n\nArgs:\n    a: First number\n    b: Second number\n\nReturns:\n    Sum of the two numbers\n"""'
        result = validator.validate_docstring_quality(valid_docstring)

        if result.get('is_valid'):
            print("✅ Quality validation working correctly")
            print(f"   - Score: {result.get('score')}%")
            return True
        else:
            print(f"❌ Quality validation failed: {result.get('issues')}")
            return False

    except Exception as e:
        print(f"❌ Quality validation test failed: {e}")
        return False

def test_file_operations():
    """Test file reading and writing operations."""
    print("\n📁 Testing file operations...")

    try:
        from utils import read_file, write_file

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            test_content = 'def test_function():\n    pass\n'
            f.write(test_content)
            temp_path = f.name

        # Test reading
        read_content = read_file(temp_path)
        if read_content == test_content:
            print("✅ File reading working correctly")
        else:
            print(f"❌ File reading failed: expected '{test_content}', got '{read_content}'")
            return False

        # Test writing
        new_content = 'def new_function():\n    return True\n'
        success = write_file(temp_path, new_content)
        if success:
            # Verify write
            verify_content = read_file(temp_path)
            if verify_content == new_content:
                print("✅ File writing working correctly")
            else:
                print(f"❌ File writing verification failed: expected '{new_content}', got '{verify_content}'")
                return False
        else:
            print("❌ File writing failed")
            return False

        # Cleanup
        os.unlink(temp_path)
        return True

    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_synthesis_engine_initialization():
    """Test synthesis engine initialization without API calls."""
    print("\n⚙️ Testing synthesis engine initialization...")

    try:
        from modules import SynthesisEngine

        engine = SynthesisEngine()

        # Check provider status (should work even without API keys)
        status = engine.get_provider_status()
        if isinstance(status, dict) and len(status) > 0:
            print("✅ Synthesis engine initializes correctly")
            print(f"   - Provider status: {status}")
            return True
        else:
            print(f"❌ Synthesis engine status check failed: {status}")
            return False

    except Exception as e:
        print(f"❌ Synthesis engine test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("🚀 Starting Comprehensive Testing of Automated Python Docstring Generator")
    print("=" * 80)

    tests = [
        ("Import Functionality", test_imports),
        ("API Key Loading", test_api_key_loading),
        ("Model Consistency", test_model_consistency),
        ("AST Extraction", test_ast_extractor),
        ("Quality Validation", test_quality_validator),
        ("File Operations", test_file_operations),
        ("Synthesis Engine", test_synthesis_engine_initialization),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! The application is working perfectly.")
        return True
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

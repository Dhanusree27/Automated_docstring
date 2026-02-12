"""
Configuration file for Automated Docstring Generator.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""

    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    

    # Docstring Style
    DEFAULT_DOCSTRING_STYLE = "google"
    SUPPORTED_STYLES = ["google", "numpy", "rest"]

    # Coverage Thresholds (percentage)
    COVERAGE_THRESHOLD_EXCELLENT = 95
    COVERAGE_THRESHOLD_GOOD = 80
    COVERAGE_THRESHOLD_FAIR = 60

    # API Configuration
    API_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    # File Configuration
    PYTHON_FILE_EXTENSIONS = [".py"]
    IGNORED_DIRECTORIES = ["__pycache__", ".git", "venv", ".venv", "node_modules"]

    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "docstring_generator.log"

    # Feature Flags
    ENABLE_AUTOFIX = True
    ENABLE_CACHING = True
    ENABLE_PARALLEL_PROCESSING = True


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG = True
    TESTING = True


def get_config() -> Config:
    """
    Get configuration based on environment.

    Returns:
        Configuration object for the current environment.
    """
    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()

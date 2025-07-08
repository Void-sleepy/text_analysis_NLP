# Configuration file for Text Analysis Tool

# Application settings
DEBUG = True
SECRET_KEY = 'your-secret-key-here-change-in-production'       # there\s no key 

# Text analysis settings
MAX_WORDS = 340
MAX_TEXT_LENGTH = 2500

# Analysis timeouts (in seconds)
ANALYSIS_TIMEOUT = 30
GRAMMAR_TIMEOUT = 20

# Rate limiting (requests per minute per IP)
RATE_LIMIT = 60

# Supported languages
SUPPORTED_LANGUAGES = ['en-US']

# Feature flags
ENABLE_SPEECH_SYNTHESIS = True
ENABLE_PLAGIARISM_CHECK = True
ENABLE_IMPROVEMENT_SUGGESTIONS = True

# API endpoints
API_BASE_URL = '/api'
ANALYZE_ENDPOINT = f'{API_BASE_URL}/analyze'
SUGGESTIONS_ENDPOINT = f'{API_BASE_URL}/suggestions'
IMPROVE_ENDPOINT = f'{API_BASE_URL}/improve'

# Static file paths
STATIC_FOLDER = 'static'
TEMPLATES_FOLDER = 'templates'

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'text_analysis.log'

"""
AI Toolkit - Unified interface for all functions
Usage: from ai import *
"""

# Import from each module
from .core import *
from .image import *
from .file_mgmt import *
from .upload import *

# Define what's available with "import *"
__all__ = [
    # Core functions
    'set_model', 'set_response', 'out', 'check_ollama_status',

    # Image functions
    'analyze_image', 'describe_image', 'ask_about_image', 
    'extract_text_from_image', 'analyze_image_light',
    'prepare_image',

    # File management functions
    'setup_ai_directory', 'list_ai_files', 'upload_to_ai',
    'read_ai_file', 'process_ai_image', 'delete_ai_file',

    # Upload functions
    'upload_file', 'upload_files_multiple'
]

print("✅ AI Toolkit loaded successfully!")
print(f"📁 Use from ai import * to access all {len(__all__)} functions")

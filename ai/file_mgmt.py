"""
File management functions for AI directory
"""
import os
import shutil
from PIL import Image
from IPython.display import display, Markdown
from .image import analyze_image

# Constants
AI_FILES_DIR = os.path.expanduser("~/ai_files")
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

def setup_ai_directory():
    """Create AI files directory"""
    if not os.path.exists(AI_FILES_DIR):
        os.makedirs(AI_FILES_DIR)
        print(f"✅ Created AI files directory: {AI_FILES_DIR}")
    return AI_FILES_DIR

def list_ai_files():
    """List files in AI directory with markdown formatting"""
    setup_ai_directory()
    files = os.listdir(AI_FILES_DIR)

    if files:
        markdown = "## 📁 Files in AI Directory\n\n"
        markdown += "| # | Type | Filename | Size |\n"
        markdown += "|---|------|----------|------|\n"

        for i, file in enumerate(files, 1):
            path = os.path.join(AI_FILES_DIR, file)
            size = os.path.getsize(path) / 1024
            size_str = f"{size:.1f} KB" if size < 1024 else f"{size/1024:.1f} MB"

            ftype = "🖼️ Image" if file.lower().endswith(('.png', '.jpg', '.jpeg')) else "📄 Text"
            markdown += f"| {i} | {ftype} | `{file}` | {size_str} |\n"

        display(Markdown(markdown))
    else:
        display(Markdown("📁 AI directory is empty"))
    return files

def upload_to_ai(source_path):
    """Upload file to AI directory"""
    setup_ai_directory()

    if not os.path.exists(source_path):
        print(f"❌ Source file not found: {source_path}")
        return False

    filename = os.path.basename(source_path)
    dest_path = os.path.join(AI_FILES_DIR, filename)

    # Handle large images
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_size = os.path.getsize(source_path)
        if file_size > MAX_IMAGE_SIZE:
            print(f"⚠️ Large image, resizing...")
            img = Image.open(source_path)
            img.thumbnail((1024, 1024))
            img.save(dest_path, quality=85)
            print(f"✅ Uploaded resized image")
            return dest_path

    shutil.copy2(source_path, dest_path)
    print(f"✅ Uploaded '{filename}'")
    return dest_path

def read_ai_file(filename):
    """Read a text file from AI directory"""
    setup_ai_directory()
    path = os.path.join(AI_FILES_DIR, filename)

    if not os.path.exists(path):
        print(f"❌ File not found: {filename}")
        return None

    with open(path, 'r') as f:
        content = f.read()

    display(Markdown(f"### 📄 {filename}\n\n```\n{content}\n```"))
    return content

def process_ai_image(filename, prompt="Describe this image"):
    """Process an image from AI directory"""
    setup_ai_directory()
    path = os.path.join(AI_FILES_DIR, filename)

    if not os.path.exists(path):
        print(f"❌ Image not found: {filename}")
        return None

    result = analyze_image(path, prompt)
    display(Markdown(f"### 🖼️ {filename}\n\n{result}"))
    return result

def delete_ai_file(filename):
    """Delete a file from AI directory"""
    setup_ai_directory()
    path = os.path.join(AI_FILES_DIR, filename)

    if os.path.exists(path):
        os.remove(path)
        print(f"✅ Deleted '{filename}'")
    else:
        print(f"❌ File not found: {filename}")

def read_ai_file_safe(filename):
    """
    Safely read a file - shows text files normally, warns for binary files
    """
    setup_ai_directory()
    path = os.path.join(AI_FILES_DIR, filename)

    if not os.path.exists(path):
        print(f"❌ File not found: {filename}")
        return None

    # Check if it's a text file
    text_extensions = ['.txt', '.md', '.csv', '.json', '.py', '.html', '.css', '.js', '.xml']
    ext = os.path.splitext(filename)[1].lower()

    if ext in text_extensions:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        display(Markdown(f"### 📄 {filename}\n\n```\n{content[:2000]}{'...' if len(content)>2000 else ''}\n```"))
        return content
    elif ext == '.pdf':
        print(f"📑 {filename} is a PDF. Use a PDF reader to view it.")
        return None
    else:
        print(f"📁 {filename} is a binary file ({ext})")
        return None

# Add PDF support
import PyPDF2

def read_pdf(filename):
    """Read a PDF file from AI directory"""
    setup_ai_directory()
    path = os.path.join(AI_FILES_DIR, filename)

    if not os.path.exists(path):
        print(f"❌ PDF not found: {filename}")
        return None

    try:
        with open(path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text += f"\n--- Page {i+1} ---\n{page_text}"

        display(Markdown(f"### 📑 {filename}\n\n```\n{text[:2000]}...\n```"))
        return text
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def read_ai_file_auto(filename):
    """Auto-detect file type and read accordingly"""
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.pdf':
        return read_pdf(filename)
    elif ext in ['.txt', '.md', '.csv', '.json', '.py']:
        return read_ai_file(filename)
    else:
        print(f"📁 Unknown file type: {ext}")
        return None

"""
Image analysis functions using BakLLaVA and moondream
"""
import os
import base64
import requests
from PIL import Image
from IPython.display import display, Markdown
from .core import set_response

# Constants
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

def prepare_image(image_path, max_size=1024):
    """
    Prepare image for AI analysis by resizing if too large
    """
    if not os.path.exists(image_path):
        return None

    file_size = os.path.getsize(image_path)
    file_size_mb = file_size / (1024 * 1024)

    img = Image.open(image_path)

    need_resize = False
    if file_size_mb > 5:
        print(f"⚠️ Image is large ({file_size_mb:.1f} MB). Resizing...")
        need_resize = True
    elif max(img.size) > max_size:
        print(f"⚠️ Image dimensions {img.size} are large. Resizing...")
        need_resize = True

    if need_resize:
        img.thumbnail((max_size, max_size))
        temp_path = "/tmp/ai_processed_image.jpg"
        img.save(temp_path, quality=85)
        print(f"✅ Resized image saved ({os.path.getsize(temp_path) / 1024:.1f} KB)")
        return temp_path
    return image_path

def analyze_image(image_path, prompt="Describe this image in detail"):
    """
    Analyze an image using BakLLaVA with automatic resizing
    """
    if not os.path.exists(image_path):
        return f"❌ Image not found: {image_path}"

    processed_path = prepare_image(image_path)
    if not processed_path:
        return "❌ Failed to process image"

    try:
        with open(processed_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')

        response = requests.post(
            'http://localhost:11434/api/chat',
            json={
                "model": "bakllava",
                "messages": [{
                    "role": "user",
                    "content": prompt,
                    "images": [image_base64]
                }],
                "stream": False,
                "options": {"num_ctx": 1024, "temperature": 0.7}
            },
            timeout=120
        )

        if processed_path != image_path and os.path.exists(processed_path):
            os.remove(processed_path)

        if response.status_code == 200:
            return response.json()['message']['content']
        return f"❌ Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"❌ Exception: {type(e).__name__}: {e}"

def describe_image(image_path):
    """Quick image description with markdown"""
    result = analyze_image(image_path, "Describe this image in detail")
    display(Markdown(f"### 📸 Image Description\n\n{result}"))
    return result

def ask_about_image(image_path, question):
    """Ask a question about an image"""
    result = analyze_image(image_path, question)
    display(Markdown(f"### ❓ Answer\n\n{result}"))
    return result

def extract_text_from_image(image_path):
    """Extract text from image"""
    result = analyze_image(image_path, "Read and extract all text visible in this image")
    display(Markdown(f"### 📝 Extracted Text\n\n{result}"))
    return result

def analyze_image_light(image_path, prompt="Describe this image"):
    """Use moondream (lighter model)"""
    try:
        processed_path = prepare_image(image_path, max_size=512)

        with open(processed_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')

        response = requests.post(
            'http://localhost:11434/api/chat',
            json={
                "model": "moondream",
                "messages": [{
                    "role": "user",
                    "content": prompt,
                    "images": [image_base64]
                }],
                "stream": False
            },
            timeout=120
        )

        if processed_path != image_path and os.path.exists(processed_path):
            os.remove(processed_path)

        if response.status_code == 200:
            result = response.json()['message']['content']
            display(Markdown(f"### 🌙 Moondream Analysis\n\n{result}"))
            return result
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

"""
Interactive file upload functions with native file picker
"""
import os
import shutil
import subprocess
from IPython.display import display, Markdown
from .file_mgmt import setup_ai_directory

def upload_file():
    """
    Open native file picker to select and upload any file
    """
    print("📂 Opening native file picker...")

    try:
        result = subprocess.run(
            ['zenity', '--file-selection', '--title=Select a file to upload'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            file_path = result.stdout.strip()
        else:
            print("❌ Upload cancelled")
            return None

    except FileNotFoundError:
        print("❌ Install zenity: sudo apt install zenity")
        return None

    if not file_path:
        print("❌ No file selected")
        return None

    # Setup and copy
    setup_ai_directory()
    filename = os.path.basename(file_path)
    dest_path = os.path.join(os.path.expanduser("~/ai_files"), filename)

    # Check if exists
    if os.path.exists(dest_path):
        response = input(f"⚠️ '{filename}' exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("❌ Upload cancelled")
            return None

    try:
        shutil.copy2(file_path, dest_path)
        size = os.path.getsize(dest_path) / 1024

        # Show markdown result
        md = f"""
## ✅ Upload Successful!

| Property | Value |
|----------|-------|
| 📂 File | `{filename}` |
| 📊 Size | {size:.1f} KB |
| 📍 Location | `{dest_path}` |
"""
        display(Markdown(md))
        return dest_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def upload_files_multiple():
    """Upload multiple files at once"""
    print("📂 Select files (Ctrl+Click for multiple)...")

    try:
        result = subprocess.run(
            ['zenity', '--file-selection', '--multiple', '--title=Select files'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            file_paths = result.stdout.strip().split('|')
        else:
            print("❌ Cancelled")
            return []

    except FileNotFoundError:
        print("❌ Install zenity: sudo apt install zenity")
        return []

    if not file_paths or file_paths == ['']:
        return []

    setup_ai_directory()
    uploaded = []

    print(f"\n📤 Uploading {len(file_paths)} files...")

    for path in file_paths:
        filename = os.path.basename(path)
        dest = os.path.join(os.path.expanduser("~/ai_files"), filename)

        try:
            shutil.copy2(path, dest)
            uploaded.append(dest)
            print(f"  ✅ {filename}")
        except Exception as e:
            print(f"  ❌ {filename}: {e}")

    print(f"\n✅ Uploaded {len(uploaded)} files")
    return uploaded

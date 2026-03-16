# AI Toolkit

A lightweight local AI toolkit for Python that makes it easy to interact with **Ollama** models for:

- **Text generation**
- **Image analysis**
- **OCR-style text extraction from images**
- **Local file management**
- **Jupyter Notebook friendly output**

This project is designed for beginners and students who want a simple way to use local AI models in Python without building everything from scratch.

---

## Features

- Simple wrapper for **Ollama text models**
- Supports **global model selection**
- Vision support with **BakLLaVA**
- Lightweight image analysis with **Moondream**
- Automatic image resizing for large uploads
- Local AI file storage (`~/ai_files`)
- Safe file reading from AI directory
- Jupyter-friendly Markdown output helpers
- Native Linux file picker support via `zenity`

---

⚪ Project Structure

```bash
ai_toolkit/
├── ai/
│   ├── __init__.py
│   ├── config.py
│   ├── core.py
│   ├── vision.py
│   ├── files.py
│   ├── ui.py
│   └── picker.py
├── requirements.txt
└── README.md


🟥 Requirements
```
Python 3.10+
•Ollama� installed and running
•Recommended models:
•llama3.1:8b (text)
•bakllava (vision)
•moondream (light vision)

Install Ollama
Install Ollama from the official website:
👉 https://ollama.com/download�
Start Ollama:
Bash
Copy code
ollama serve
Pull the recommended models:
Bash
Copy code
ollama pull llama3.1:8b
ollama pull bakllava
ollama pull moondream
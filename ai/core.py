"""
Core text AI functions
"""
import requests
import os
from IPython.display import display, Markdown

# Global variable to store current model
_current_model = None

def check_ollama_status():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama is running!")
            print("\n📦 Installed models:")
            for model in models['models']:
                print(f"   - {model['name']}")
            return True
        else:
            print("❌ Ollama is not responding properly")
            return False
    except:
        print("❌ Cannot connect to Ollama. Make sure it's running with 'ollama serve'")
        return False

def set_model(model_name):
    """Set the global model"""
    global _current_model
    _current_model = model_name
    print(f"✅ Global model set to: {model_name}")

def set_response(prompt, model=None):
    """Get AI response without printing"""
    global _current_model
    use_model = model or _current_model
    if not use_model:
        return "❌ No model set! Use set_model() first"

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": use_model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            return result['response']
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

def out(prompt, model=None):
    """Get AI response with markdown formatting"""
    response = set_response(prompt, model)
    if response and not response.startswith("❌"):
        display(Markdown(response))
        print()
    return response

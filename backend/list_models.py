from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Gemini Models:\n")

try:
    models = client.models.list()
    for model in models:
        print(f"{model.name}")
        if hasattr(model, 'display_name'):
            print(f"   Display: {model.display_name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"   Methods: {', '.join(model.supported_generation_methods)}")
        print()
except Exception as e:
    print(f"Error: {e}")

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()

for model in models:
    print(model.name, "|", "generation" if "generateContent" in model.supported_generation_methods else "")

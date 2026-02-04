import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Грешка: Няма API ключ в .env файла!")
else:
    genai.configure(api_key=API_KEY)
    print("--- Налични Gemini Модели за твоя ключ ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Name: {m.name}")
    except Exception as e:
        print(f"Грешка при свързване: {e}")
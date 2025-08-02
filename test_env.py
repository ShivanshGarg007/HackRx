from dotenv import load_dotenv
load_dotenv()
import os
print("Gemini API Key from test_env.py:", os.getenv("GEMINI_API_KEY"))
from dotenv import load_dotenv
load_dotenv()
import os
from typing import Dict

try:
    import google.generativeai as genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    genai = None

try:
    import openai
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
except ImportError:
    openai = None

try:
    from mistralai.client import MistralClient
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    mistral_client = MistralClient(api_key=MISTRAL_API_KEY) if MISTRAL_API_KEY else None
except ImportError:
    mistral_client = None

def parse_query_with_llm(query: str) -> Dict:
    """
    Use Gemini (preferred), OpenAI, or Mistral to parse the user query into structured fields.
    Returns a dict with keys: age, gender, procedure, location, policy_duration, etc.
    """
    prompt = f"""
    Extract the following fields from the insurance query below:
    - Age
    - Gender
    - Procedure
    - Location
    - Policy Duration
    If any field is missing, return null for that field.
    Query: {query}
    Return as JSON.
    """
    # Try Gemini first
    if genai and GEMINI_API_KEY:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        try:
            import json
            return json.loads(response.text)
        except Exception:
            return {"error": "Failed to parse Gemini response"}
    # Fallback to OpenAI
    elif openai and OPENAI_API_KEY:
        completion = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            import json
            return json.loads(completion.choices[0].message["content"])
        except Exception:
            return {"error": "Failed to parse OpenAI response"}
    # Fallback to Mistral
    elif mistral_client and MISTRAL_API_KEY:
        print("Calling Mistral API...")
        response = mistral_client.chat(
            model="mistral-tiny",
            messages=[{"role": "user", "content": prompt}]
        )
        print("Mistral API response received.")
        try:
            import json
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {"error": "Failed to parse Mistral response"}
    else:
        return {"error": "No LLM API key configured"} 
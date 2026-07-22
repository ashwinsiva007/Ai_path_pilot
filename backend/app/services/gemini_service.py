import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Updated to use gemini-3.5-flash which is active in this environment
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    def generate_content(self, prompt: str) -> str:
        url = f"{GEMINI_API_URL}?key={self.api_key}"
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def extract_resume_data(self, text: str) -> dict:
        prompt = f"""
Extract the following information from the resume text below.
Return ONLY a raw JSON object (no markdown, no code fences) with this schema:
{{
    "Name": "string",
    "Skills": ["string"],
    "Projects": [{{"title": "string", "description": "string"}}],
    "Education": ["string"],
    "Certifications": ["string"],
    "Experience": ["string"],
    "Interests": ["string"],
    "Career Domain": "string",
    "Resume Score": 85,
    "Career Readiness": "string"
}}

Resume Text:
{text}
"""
        response_text = self.generate_content(prompt)
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        try:
            return json.loads(response_text.strip())
        except Exception as e:
            print("Failed to parse resume JSON:", str(e))
            return {}

# Singleton
gemini_service = GeminiService()

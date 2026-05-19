import os
import json
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Fallback models
MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite"
]


def analyze_report(report_text):

    prompt = f"""
You are an AI-powered medical report analysis assistant.

Analyze the following medical report carefully.

Instructions:
1. Identify abnormal values
2. Explain findings simply
3. Estimate overall risk level
4. Suggest precautions
5. Do NOT provide a final medical diagnosis
6. Return ONLY valid JSON
7. Do not include markdown formatting

Return JSON in this exact format:

{{
  "patient_name": "",
  "abnormalities": [],
  "risk_level": "",
  "summary": "",
  "precautions": []
}}

Medical Report:
{report_text}
"""

    response = None

    # Try multiple Gemini models
    for model_name in MODELS:

        try:

            print(f"Trying model: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            print(f"Success using: {model_name}")

            break

        except Exception as e:

            print(f"Model failed: {model_name}")
            print(e)

            time.sleep(3)

    # All models failed
    if response is None:

        return {
            "error": "All Gemini models failed"
        }

    raw_response = response.text.strip()

    # Remove markdown formatting if model adds it
    raw_response = raw_response.replace("```json", "")
    raw_response = raw_response.replace("```", "")
    raw_response = raw_response.strip()

    try:

        parsed_json = json.loads(raw_response)

        return parsed_json

    except json.JSONDecodeError:

        return {
            "error": "Invalid JSON returned by Gemini",
            "raw_response": raw_response
        }
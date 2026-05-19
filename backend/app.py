import os
import shutil
import traceback
import requests

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ocr import extract_text
from gemini_agent import analyze_report

app = FastAPI(
    title="Medical AI Analyzer",
    description="AI-powered medical report analysis system",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory
UPLOAD_DIR = "uploaded_reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():

    return {
        "message": "Medical AI Analyzer API Running"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    try:

        # Clean filename
        filename = file.filename.replace(" ", "_")

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"Saved file: {file_path}")

        # OCR extraction
        report_text = extract_text(file_path)

        print("OCR completed")

        # Empty OCR check
        if not report_text.strip():

            return JSONResponse(
                status_code=400,
                content={
                    "error": "OCR could not extract text"
                }
            )

        # AI analysis
        analysis = analyze_report(report_text)

        print("Gemini analysis completed")

        # Gemini/API errors
        if "error" in analysis:

            return JSONResponse(
                status_code=429,
                content=analysis
            )

        # Trigger n8n ONLY if risk is high
        if analysis.get("risk_level") == "High":

            try:

                response = requests.post(
                    "http://n8n:5678/webhook/high-risk",
                    json=analysis,
                    timeout=10
                )

                print(
                    f"n8n webhook triggered: {response.status_code}"
                )

            except Exception as n8n_error:

                print("Failed to trigger n8n webhook")
                print(n8n_error)

        # Final API response
        return {
            "filename": filename,
            "analysis": analysis
        }

    except Exception as e:

        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "details": str(e)
            }
        )
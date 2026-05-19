from ocr import extract_text
from gemini_agent import analyze_report

image_path = "../uploads/report.png"

# OCR extraction
report_text = extract_text(image_path)

print("\n===== EXTRACTED TEXT =====\n")
print(report_text)

# Gemini analysis
print("\n===== AI ANALYSIS =====\n")

analysis = analyze_report(report_text)

print(analysis)
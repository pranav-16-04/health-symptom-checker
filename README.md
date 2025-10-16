# 🩺 Healthcare Symptom Checker (Streamlit)

An AI-powered symptom checker built with Streamlit that uses Google Gemini to analyze free‑text symptom descriptions and returns:

- Severity assessment (Low/Moderate/High)
- Urgent care guidance (if any)
- Possible conditions
- General recommendations
- Confidence score with justification
- A clear medical disclaimer

This app runs locally via Streamlit (no Flask server required).

> Disclaimer: This tool is for informational/educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment.

## What’s in this repo

- app.py — Main Streamlit app (uses GEMINI_API_KEY environment variable)
- check_models.py — Streamlit utility to verify Gemini API configuration and list usable models (reads from Streamlit secrets)
- templates/index.html — Legacy static page intended for a Flask backend; it is not used by the Streamlit app
- .streamlit/secrets.toml — Local secrets file (ignored by Git via .gitignore); do not commit your real key
- requirements.txt — Python dependencies

## Prerequisites

- Python 3.9+ (3.10+ recommended)
- A Google Gemini API key

## Setup (Windows PowerShell)

1) Clone and enter the project directory

powershell
git clone <your-repo-url>
cd Health-Symptom-Checker-main


2) Create and activate a virtual environment

powershell
python -m venv .venv
.\.venv\Scripts\Activate


3) Install dependencies

powershell
pip install -r requirements.txt


4) Configure your Gemini API key
    - Create a file at .streamlit/secrets.toml with:
    
        GEMINI_API_KEY = "your_api_key_here"
        
    - check_models.py expects the key here.


    

## Run the app

powershell
streamlit run app.py


Then open the local URL displayed in the terminal (typically http://localhost:8501). Enter your symptoms and click “Analyze”.

### Optional: Verify your Gemini setup and list models

powershell
streamlit run check_models.py


This utility loads GEMINI_API_KEY from Streamlit secrets and displays usable generative models.

## Notes on models

- The app uses model ID models/gemini-2.5-flash in app.py.
- If your account/region doesn’t have access to that model, update the model ID in app.py to one your key can use (e.g., a different Gemini “flash” or “pro” variant). You can use check_models.py to see available models.

## Troubleshooting

- Missing API key
    - app.py and check_models.py requires the GEMINI_API_KEY in .streamlit/secrets.toml.

- “The model did not return valid JSON”
    - The app tries to parse the model output as JSON. If parsing fails, the raw response is shown.
    - Try clicking Analyze again, refining the symptom text, or tightening the prompt JSON schema in app.py if needed.

- Network/region access
    - Ensure the Gemini API is available in your region and your key has the right permissions.

## Security and repository hygiene

- Do NOT commit real API keys. The .gitignore ignores .streamlit/, but if a secrets file was committed previously, rotate that key immediately and remove the file from version control history.
- Keep your local .streamlit/secrets.toml out of Git. Treat it like a password vault entry.

## Architecture summary

- Streamlit handles the UI, eventing, and rendering — no separate web server is needed.
- On “Analyze”, app.py calls Gemini with a strict JSON schema, renders severity/conditions/guidance/confidence, and shows a disclaimer.

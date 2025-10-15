import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime

# Load Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.title("🩺 AI Symptom Checker")

symptoms = st.text_area("Enter your symptoms:")
if st.button("Analyze"):
    if symptoms.strip():
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        prompt = f"""
        Analyze the user's symptoms and return a single, valid JSON object with the exact nested schema defined below.
        Context: Today is {datetime.now().strftime('%Y-%m-%d')}. User is in Vijayawada, India.
        Symptoms: "{symptoms}"
        JSON Output Schema:
        {{
          "analysis": {{
            "severity_assessment": "(Low/Moderate/High)",
            "confidence_score": "(Low/Medium/High)",
            "confidence_justification": "(Reason)"
          }},
          "guidance": {{
            "urgent_care_needed": [],
            "general_recommendations": []
          }},
          "medical_information": {{
            "possible_conditions": []
          }},
          "disclaimer": "This is for informational purposes only and is not a substitute for professional medical advice. Please consult a healthcare provider for a diagnosis."
        }}
        """

        # 🔹 Generate response
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # 🧹 Clean Markdown formatting if present
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()

        # ...existing code...
        try:
            data = json.loads(response_text)
            
            # Severity Card
            severity = data["analysis"]["severity_assessment"]
            severity_color = {
                "Low": "#d1e7dd",
                "Moderate": "#fff3cd",
                "High": "#f8d7da"
            }.get(severity, "#f8f9fa")
            st.markdown(
                f"<div style='background:{severity_color};padding:16px;color:#212529;border-radius:8px;font-weight:bold;text-align:center;'>"
                f"Severity Assessment: {severity}</div>", unsafe_allow_html=True
            )

            # Urgent Care Card
            urgent = data["guidance"]["urgent_care_needed"]
            if urgent:
                st.markdown(
                    "<div style='border:2px solid #dc3545;background:#f8d7da1a;padding:16px;border-radius:8px;'>"
                    "<h4 style='color:#dc3545;'>⚠️ Urgent Care Recommended</h4>"
                    "<ul style='color:#dc3545;'>"
                    + "".join(f"<li>{item}</li>" for item in urgent) +
                    "</ul></div>", unsafe_allow_html=True
                )

            # Probable Conditions
            st.markdown(
                "<div style='background:#fff;color:#212529;padding:16px;border-radius:8px;margin-top:12px;'>"
                "<h4>🩺 Probable Conditions</h4>"
                "<ul>"
                + "".join(f"<li>{item}</li>" for item in data["medical_information"]["possible_conditions"]) +
                "</ul></div>", unsafe_allow_html=True
            )

            # General Recommendations
            st.markdown(
                "<div style='background:#fff;color:#212529;padding:16px;border-radius:8px;margin-top:12px;'>"
                "<h4>📝 General Recommendations</h4>"
                "<ul>"
                + "".join(f"<li>{item}</li>" for item in data["guidance"]["general_recommendations"]) +
                "</ul></div>", unsafe_allow_html=True
            )

            # Confidence Score
            st.markdown(
                "<div style='background:#f8f9fa;color:#212529;padding:16px;border-radius:8px;margin-top:12px;'>"
                f"<h4>📊 Analysis Confidence: {data['analysis']['confidence_score']}</h4>"
                f"<p style='font-style:italic;color:#6c757d;'>{data['analysis']['confidence_justification']}</p>"
                "</div>", unsafe_allow_html=True
            )

            # Disclaimer
            st.markdown(
                "<div style='background:#fff3cd;color:#212529;padding:16px;border-radius:8px;margin-top:12px;border-left:5px solid #ffc107;'>"
                f"{data['disclaimer']}</div>", unsafe_allow_html=True
            )
        except json.JSONDecodeError:
            st.error("⚠️ The model did not return valid JSON. Showing raw response instead:")
            st.code(response_text)
    else:
        st.warning("Please enter some symptoms first.")

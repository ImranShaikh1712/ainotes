import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from fpdf import FPDF

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  # Change back to 2.5-pro when quota resets

# Set Streamlit page config
st.set_page_config(page_title="AI Notes Generator", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .stTextArea textarea {
            background-color: #1e1e1e !important;
            color: white !important;
            border: 1px solid #4CAF50 !important;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            padding: 0.6em 1.2em;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📝 AI NOTES ")
st.subheader("Paste your topic or content below:")

input_text = st.text_area("Enter your topic or lecture content")

# Generate notes
if st.button("Generate Notes"):
    if input_text.strip():
        with st.spinner("Generating notes..."):
            try:
                response = model.generate_content(input_text)
                output = response.text
                st.success("✅ Notes generated successfully!")
                st.text_area("🧠 AI-Generated Notes", value=output, height=300, key="output")

                # Download as PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                for line in output.split('\n'):
                    pdf.multi_cell(0, 10, line)
                pdf_output = "notes.pdf"
                pdf.output(pdf_output)

                with open(pdf_output, "rb") as file:
                    st.download_button("📥 Download Notes as PDF", file, file_name="notes.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"❌ An error occurred:\n\n{e}")
    else:
        st.warning("⚠️ Please enter some input before generating notes.")

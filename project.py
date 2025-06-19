import streamlit as st
import fitz  # PyMuPDF
import difflib
import tempfile
import os
import pyttsx3
import speech_recognition as sr

# Optional fallback if spaCy fails
def extract_name_fallback(text):
    # Very simple name guesser using the first line or common patterns
    lines = text.strip().split("\n")
    for line in lines:
        if "name" in line.lower():
            return line.strip().split(":")[-1].strip()
    return lines[0] if lines else "Unknown"

# Extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

# Get closest matching sentence from PDF
def get_closest_match(question, text):
    sentences = text.split(".")
    return difflib.get_close_matches(question, sentences, n=1, cutoff=0.3)[0] if sentences else ""

# Voice input (optional use)
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for your question...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        st.success(f"You said: {query}")
        return query
    except Exception as e:
        st.error("Could not understand. Try again.")
        return ""

# Voice output
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Streamlit UI
st.set_page_config(page_title="PDF QA App", layout="centered")
st.title("📄 PDF Question Answer Checker with Voice")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    st.success("PDF Loaded Successfully!")
    pdf_text = extract_text_from_pdf(uploaded_file)

    # Question input
    st.write("🎤 You can type or use voice input for your question")
    use_voice = st.checkbox("Use Voice Input")

    if use_voice:
        question = recognize_speech()
    else:
        question = st.text_input("Type your Question here:")

    user_answer = st.text_area("Type your Answer here:")

    if st.button("Check My Answer") and question and user_answer:
        closest_content = get_closest_match(question, pdf_text)
        st.subheader("🔍 Closest content from PDF:")
        st.info(closest_content)

        # Simple keyword comparison
        missed_keywords = [word for word in closest_content.lower().split() if word not in user_answer.lower()]
        if missed_keywords:
            st.warning("⚠️ You missed these keywords:")
            st.write(", ".join(missed_keywords))
        else:
            st.success("✅ Your answer looks good!")

        speak("Your answer has been checked!")

    # Extract name from resume
    if st.button("👤 What is the name of the candidate?"):
        name = extract_name_fallback(pdf_text)
        st.success(f"The name might be: {name}")
        speak(f"The name might be {name}")

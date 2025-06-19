import streamlit as st
import fitz  # PyMuPDF
import speech_recognition as sr

# --- Utilities ---

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Simple keyword overlap comparison
def compare_answers(user_answer, pdf_text):
    user_words = set(user_answer.lower().split())
    pdf_words = set(pdf_text.lower().split())

    matched_keywords = user_words.intersection(pdf_words)
    missing_keywords = pdf_words - user_words

    score = len(matched_keywords) / (len(pdf_words) + 1) * 100
    return score, matched_keywords, missing_keywords

# Voice input using speech_recognition
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now.")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        st.success(f"You said: {query}")
        return query
    except Exception as e:
        st.error("❌ Could not understand your voice. Try again.")
        return ""

# Naive name extractor
def extract_name_simple(text):
    for line in text.split("\n"):
        if "name" in line.lower():
            return line.split(":")[-1].strip()
    return text.split("\n")[0]

# --- Streamlit UI ---

st.set_page_config(page_title="PDF QA Feedback App", layout="centered")
st.title("📑 PDF Question & Answer Evaluator (Cloud Compatible)")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF text extracted successfully!")

    use_voice = st.checkbox("🎤 Use voice to ask the question")
    if use_voice:
        question = recognize_speech()
    else:
        question = st.text_input("🧠 Enter your question:")

    user_answer = st.text_area("✍️ Enter your answer here:")

    if st.button("Evaluate Answer") and user_answer:
        score, matched, missed = compare_answers(user_answer, pdf_text)

        st.subheader("📊 Feedback:")
        st.write(f"**Match Score**: {score:.2f}%")
        st.write(f"✅ Matched Keywords: {', '.join(matched)}")
        st.write(f"❌ Missing Keywords: {', '.join(missed)}")

    if st.button("👤 Detect Name from Resume"):
        name = extract_name_simple(pdf_text)
        st.success(f"Candidate name might be: **{name}**")

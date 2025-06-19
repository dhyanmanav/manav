import streamlit as st
import fitz  # PyMuPDF
import speech_recognition as sr

# --- Utilities ---

# Extract all text from PDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Search best matching paragraph for a given question
def search_answer_from_pdf(question, pdf_text):
    question_words = set(question.lower().split())
    best_match = ""
    best_score = 0

    for para in pdf_text.split("\n"):
        para_words = set(para.lower().split())
        common = question_words.intersection(para_words)
        score = len(common)

        if score > best_score:
            best_score = score
            best_match = para.strip()

    return best_match if best_match else "❌ No relevant answer found in the PDF."

# Recognize voice question using microphone
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Please ask your question.")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio)
        st.success(f"🗣️ You said: {query}")
        return query
    except Exception:
        st.error("❌ Sorry, could not recognize your voice. Try again.")
        return ""

# Extract name (optional)
def extract_name_simple(text):
    for line in text.split("\n"):
        if "name" in line.lower():
            return line.split(":")[-1].strip()
    return text.split("\n")[0]

# --- Streamlit UI ---

st.set_page_config(page_title="PDF Answer Finder", layout="centered")
st.title("🔍 Ask a Question & Get Answer from PDF")

uploaded_file = st.file_uploader("📄 Upload a PDF file", type=["pdf"])

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF loaded and text extracted!")

    use_voice = st.checkbox("🎤 Use voice to ask a question")
    if use_voice:
        question = recognize_speech()
    else:
        question = st.text_input("❓ Enter your question:")

    if st.button("🔎 Find Answer") and question:
        answer = search_answer_from_pdf(question, pdf_text)
        st.subheader("📘 Answer from PDF:")
        st.info(answer)

    if st.button("👤 Detect Name from Resume"):
        name = extract_name_simple(pdf_text)
        st.success(f"Candidate name might be: **{name}**")

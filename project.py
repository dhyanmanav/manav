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

# Find best matching paragraph for the question
def find_best_matching_text(question, pdf_text):
    question_words = set(question.lower().split())
    best_match = ""
    max_overlap = 0

    for para in pdf_text.split("\n"):
        para_words = set(para.lower().split())
        common = question_words.intersection(para_words)
        if len(common) > max_overlap:
            max_overlap = len(common)
            best_match = para

    return best_match

# Determine if user's answer is close enough
def is_answer_correct(user_answer, correct_text):
    user_words = set(user_answer.lower().split())
    correct_words = set(correct_text.lower().split())
    match = user_words.intersection(correct_words)

    score = len(match) / (len(correct_words) + 1) * 100  # +1 avoids divide-by-zero
    return score, score >= 60  # 60% threshold for "You're right"

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

# Naive name extractor from resume
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

    if st.button("Evaluate Answer") and user_answer and question:
        best_answer = find_best_matching_text(question, pdf_text)
        score, is_correct = is_answer_correct(user_answer, best_answer)

        st.subheader("📊 Feedback:")
        if is_correct:
            st.success("✅ You're right!")
            st.write(f"🎯 Match Score: {score:.2f}%")
        else:
            st.error("❌ Not quite correct.")
            st.write(f"🎯 Match Score: {score:.2f}%")
            st.info(f"📖 Correct answer might be:\n\n{best_answer}")

    if st.button("👤 Detect Name from Resume"):
        name = extract_name_simple(pdf_text)
        st.success(f"Candidate name might be: **{name}**")

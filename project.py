import streamlit as st
import PyPDF2
import speech_recognition as sr
from gtts import gTTS
import os
import spacy
from io import BytesIO

nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="Smart PDF QA", layout="centered")
st.title("🎙️ Voice-Enabled PDF Question Answer Checker")

# PDF Upload
pdf_file = st.file_uploader("📤 Upload your Notes PDF", type=['pdf'])

def text_to_speech(text):
    tts = gTTS(text)
    tts.save("feedback.mp3")
    audio_file = open("feedback.mp3", "rb")
    st.audio(audio_file.read(), format='audio/mp3')

def voice_input(label):
    st.write(f"🎙️ {label}")
    if st.button(f"Start Recording for {label}"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success("Captured: " + text)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError:
            st.error("Could not request results.")
    return ""

if pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    pdf_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pdf_text += page_text
    st.success("✅ PDF Loaded Successfully!")

    option = st.radio("Choose input mode:", ("Type", "Voice"))

    if option == "Type":
        question_input = st.text_input("❓ Type your Question:")
        answer_input = st.text_input("📝 Type your Answer:")
    else:
        question_input = voice_input("Question")
        answer_input = voice_input("Answer")

    if st.button("Check My Answer"):
        paragraphs = pdf_text.split('\n')
        best_para = ""
        best_score = 0
        question_doc = nlp(question_input.lower())

        for para in paragraphs:
            para_doc = nlp(para.lower())
            score = question_doc.similarity(para_doc)
            if score > best_score:
                best_score = score
                best_para = para

        st.markdown("### 🔍 Closest content from PDF:")
        st.info(best_para)

        answer_words = set(w.text.lower() for w in nlp(answer_input))
        expected_words = set(w.text.lower() for w in nlp(best_para))
        missed = expected_words - answer_words

        if missed:
            feedback = "You missed the following important keywords: " + ", ".join(missed)
            st.warning("⚠️ " + feedback)
            text_to_speech(feedback)
        else:
            st.success("🎉 Excellent! You covered all the key concepts.")
            text_to_speech("Excellent! You covered all the key concepts.")
else:
    st.info("📄 Please upload a PDF to begin.")

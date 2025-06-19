import streamlit as st
import PyPDF2
import spacy
from gtts import gTTS
import os

st.set_page_config(page_title="Voice Revision Web App", page_icon="📄")
st.title("📚 Voice Revision Web App (Cloud Version)")
st.write("Upload a PDF, type your question and answer, and get feedback with optional voice output!")

# Load spaCy model
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

# PDF Upload
pdf_file = st.file_uploader("📄 Upload your Notes PDF", type=['pdf'])

if pdf_file is not None:
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    st.success("✅ PDF Loaded Successfully!")

    question_input = st.text_input("❓ Type your Question here:")
    answer_input = st.text_area("📝 Type your Answer here:")

    if st.button("Check My Answer"):
        paragraphs = text.split('\n')
        best_match = ""
        max_matches = 0
        question_words = question_input.lower().split()

        for para in paragraphs:
            matches = sum(1 for word in question_words if word in para.lower())
            if matches > max_matches:
                max_matches = matches
                best_match = para

        if best_match:
            st.markdown("### 🔎 Closest content from PDF:")
            st.info(best_match)

            # NLP comparison
            expected_doc = nlp(best_match.lower())
            answer_doc = nlp(answer_input.lower())

            expected_words = {token.lemma_ for token in expected_doc if not token.is_stop and token.is_alpha}
            answer_words = {token.lemma_ for token in answer_doc if not token.is_stop and token.is_alpha}

            missed_keywords = expected_words - answer_words

            if missed_keywords:
                st.warning("⚠️ You missed these keywords: " + ', '.join(missed_keywords))
            else:
                st.success("🎉 Great job! You covered all the important keywords.")

            # Optional voice output
            if st.checkbox("🔊 Play Answer Feedback (Text-to-Speech)"):
                feedback = f"You missed the keywords: {', '.join(missed_keywords)}" if missed_keywords else "Great job! You covered everything."
                tts = gTTS(feedback)
                tts.save("feedback.mp3")
                st.audio("feedback.mp3", format="audio/mp3")
        else:
            st.error("❌ No relevant content found in the PDF.")
else:
    st.info("📥 Please upload a PDF to begin.")

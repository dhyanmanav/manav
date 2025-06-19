import streamlit as st
import PyPDF2

# Title and intro
st.set_page_config(page_title="Voice Revision Web App (Demo)", layout="centered")
st.title("📘 Voice Revision Web App (Demo)")
st.write("Upload a **PDF** of your notes, type your **question** and **your answer**, and receive keyword feedback!")

# PDF Upload
pdf_file = st.file_uploader("📤 Upload your Notes PDF", type=['pdf'])

if pdf_file is not None:
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        st.success("✅ PDF Loaded Successfully!")

        # User Question
        question_input = st.text_input("❓ Type your Question here:")

        # User Answer
        answer_input = st.text_input("📝 Type your Answer here:")

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

            if best_match.strip():
                st.markdown("### 🔍 Closest content from PDF:")
                st.info(best_match)

                expected_words = set(best_match.lower().split())
                user_words = set(answer_input.lower().split())
                missed = expected_words - user_words

                if missed:
                    st.warning("⚠️ You missed these keywords:\n\n" + ', '.join(missed))
                else:
                    st.success("🎉 Great job! You covered all the keywords.")
            else:
                st.error("❌ No matching content found in PDF.")
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
else:
    st.info("👆 Please upload a PDF to begin.")

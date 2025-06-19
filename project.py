import streamlit as st
import fitz  # PyMuPDF
import re
import math
from collections import Counter

# ----------- Utility Functions -----------

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def tokenize(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    return text.split()

def term_frequency(words):
    return Counter(words)

def cosine_similarity(text1, text2):
    words1 = tokenize(text1)
    words2 = tokenize(text2)

    tf1 = term_frequency(words1)
    tf2 = term_frequency(words2)

    all_words = set(tf1.keys()).union(set(tf2.keys()))
    vec1 = [tf1.get(word, 0) for word in all_words]
    vec2 = [tf2.get(word, 0) for word in all_words]

    dot = sum(x * y for x, y in zip(vec1, vec2))
    mag1 = math.sqrt(sum(x ** 2 for x in vec1))
    mag2 = math.sqrt(sum(y ** 2 for y in vec2))

    return dot / (mag1 * mag2 + 1e-9)  # Avoid divide by zero

def find_all_relevant_paragraphs(question, paragraphs, threshold=0.2):
    matches = []
    for para in paragraphs:
        score = cosine_similarity(question, para)
        if score >= threshold:
            matches.append((para.strip(), score))
    # Sort by score (high to low)
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

# ----------- Streamlit UI -----------

st.set_page_config("📚 AI PDF Chatbot", layout="centered")
st.title("🤖 PDF Chatbot: Get All Relevant Answers")

uploaded_file = st.file_uploader("📂 Upload a PDF", type=["pdf"])

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF loaded successfully!")

    paragraphs = [p.strip() for p in raw_text.split("\n") if len(p.strip()) > 40]
    st.info(f"🔍 Loaded {len(paragraphs)} searchable paragraphs.")

    question = st.text_input("❓ Ask your question:")

    if st.button("🔎 Find All Answers") and question:
        results = find_all_relevant_paragraphs(question, paragraphs)

        st.subheader("📘 Relevant Answers:")
        if results:
            for i, (para, score) in enumerate(results, 1):
                st.markdown(f"**{i}. (Score: {score:.3f})**\n\n{para}\n---")
        else:
            st.error("❌ No relevant answers found in the PDF.")

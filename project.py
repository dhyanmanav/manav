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
            text += page.get_text("text") + "\n"
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

    all_words = set(tf1.keys()).union(tf2.keys())
    vec1 = [tf1.get(word, 0) for word in all_words]
    vec2 = [tf2.get(word, 0) for word in all_words]

    dot = sum(x * y for x, y in zip(vec1, vec2))
    mag1 = math.sqrt(sum(x ** 2 for x in vec1))
    mag2 = math.sqrt(sum(y ** 2 for y in vec2))

    return dot / (mag1 * mag2 + 1e-9)

# Split into full topics using double newlines or blocks
def split_into_topic_blocks(text):
    blocks = re.split(r'\n{2,}', text)
    return [block.strip() for block in blocks if len(block.strip()) > 40]

# Find multiple relevant topic blocks
def find_relevant_blocks(question, blocks, threshold=0.2):
    results = []
    for block in blocks:
        score = cosine_similarity(question, block)
        if score >= threshold:
            results.append((block.strip(), score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

# ----------- Streamlit UI -----------

st.set_page_config("📚 Smart PDF Chatbot", layout="centered")
st.title("🤖 Smart PDF Chatbot (Full-Topic Answers)")

uploaded_file = st.file_uploader("📂 Upload your PDF", type=["pdf"])

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF text successfully extracted!")

    blocks = split_into_topic_blocks(pdf_text)
    st.info(f"🔍 Prepared {len(blocks)} topic blocks for semantic search.")

    question = st.text_input("❓ Ask your question:")

    if st.button("🔎 Get Full Answers") and question:
        matches = find_relevant_blocks(question, blocks)

        st.subheader("📘 Relevant Topic Answers:")
        if matches:
            for i, (block, score) in enumerate(matches, 1):
                st.markdown(f"### {i}. (Score: {score:.2f})")
                st.markdown(block)
                st.markdown("---")
        else:
            st.error("❌ Sorry, no relevant topic found in the PDF.")

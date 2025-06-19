import streamlit as st
import fitz  # PyMuPDF
import re
import math
from collections import Counter

# ----------- Utility Functions -----------

# Extract all text from PDF
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Clean and tokenize text
def tokenize(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    return text.split()

# Compute term frequency
def term_frequency(words):
    return Counter(words)

# Compute cosine similarity between two texts
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

    return dot / (mag1 * mag2 + 1e-9)  # Avoid division by zero

# Search best-matching paragraph
def find_best_answer(question, paragraphs, threshold=0.2):
    best_para = ""
    best_score = 0

    for para in paragraphs:
        score = cosine_similarity(question, para)
        if score > best_score:
            best_score = score
            best_para = para

    if best_score >= threshold:
        return best_para.strip(), best_score
    else:
        return None, best_score

# ----------- Streamlit UI -----------

st.set_page_config("📚 AI PDF Chatbot", layout="centered")
st.title("🤖 Smart PDF Chatbot (Offline, No AI Model)")

uploaded_file = st.file_uploader("📂 Upload a PDF to train the bot", type=["pdf"])

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF successfully read!")

    # Pre-split into paragraphs
    paragraphs = [p.strip() for p in raw_text.split("\n") if len(p.strip()) > 40]

    st.info(f"🔍 Loaded {len(paragraphs)} paragraphs for search.")

    question = st.text_input("❓ Ask a question related to the PDF")

    if st.button("💬 Get Answer") and question:
        answer, score = find_best_answer(question, paragraphs)

        st.subheader("🧠 Answer:")
        if answer:
            st.success(answer)
            st.caption(f"📈 Relevance score: {score:.3f}")
        else:
            st.error("❌ Sorry, I couldn’t find a relevant answer in the PDF.")

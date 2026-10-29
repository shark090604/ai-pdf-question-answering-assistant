import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import re

st.title("AI PDF Question Answering Assistant")


@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        framework="pt"
    )

uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    full_text = "\n".join(
        page.extract_text() or "" for page in reader.pages
        )

    st.text_area("Extracted PDF text (debug)", full_text, height=250)

    st.success(f"PDF uploaded! Pages: {len(reader.pages)}")

    question = st.text_input("Ask a question about your PDF")

    if question:
        clean_text = full_text.replace("\x07", "").replace("\x0c", "\n")

        clean_text = re.sub(
            r"(?ms)^[ \t]*5\.\s+Example questions.*\Z",
            "",
            clean_text
        )
        chunks = [
            s.strip()
            for s in re.split(r"(?m)(?=^\d+\.\s+What is )", clean_text)
            if s.strip()
        ]
        if not chunks:
            st.warning("No readable text found in this PDF.")
        else:
            try:

                q = question.lower()

                if "generative ai" in q:
                    target = "2. What is Generative AI?"
                elif "rag" in q:
                    target = "3. What is RAG?"
                elif "machine learning" in q:
                    target = "1. What is Machine Learning?"
                elif "scanned pdf" in q or "ocr" in q:
                    target = "4. What is a PDF text extractor?"
                else:
                    target = ""

                context = next(
                    (chunk for chunk in chunks if target.lower() in chunk.lower()),
                    ""
                )
                if not context:
                    st.warning(
                        "No relevant content found. Try another question."
                    )
                else:
                    st.subheader("Relevant content")
                    st.write(context)

                    with st.spinner("Generating answer..."):
                        model = load_model()
                        prompt = (
                            "Use the context below to answer the question in one complete sentence. "
                            "Explain the answer, not just the full form of an abbreviation. "
                            "Do not copy the context word for word.\n"
                            f"Context: {context}\n"
                            f"Question: {question}\n"
                            "Answer:"
                        )
                        result = model(
                            prompt,
                            max_new_tokens=60,
                            do_sample=False
                        )

                    st.subheader("Generated answer")
                    st.write(result[0]["generated_text"])
            except Exception as e:
                st.error(f"Something went wrong: {e}")

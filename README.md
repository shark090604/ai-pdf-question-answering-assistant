# AI PDF Question Answering Assistant

An AI-powered application that lets users upload a PDF document and ask questions about its content.

## Features
- Upload PDF documents
- Extract PDF text using pypdf
- Retrieve relevant text passages
- Generate answers using Hugging Face FLAN-T5 Small
- Interactive Streamlit interface

## Tech Stack
- Python
- Streamlit
- pypdf
- scikit-learn
- Hugging Face Transformers
- PyTorch

## Installation

Clone the repository:

    git clone https://github.com/shark090604/ai-pdf-question-answering-assistant.git
    cd ai-pdf-question-answering-assistant

Create a virtual environment and install dependencies:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Run the Application

    streamlit run app.py

Upload a text-based PDF, enter a question, and read the generated answer.

## Limitations
- Scanned PDFs may require OCR.
- Answers depend on the document content and retrieved passages.
- Generated answers may occasionally be incorrect.

## Author
GitHub: https://github.com/shark090604

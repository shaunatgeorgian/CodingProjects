import streamlit as st
import os
import requests
from PyPDF2 import PdfReader
import llama_index 

# Initialize Llama Index
llama = llama_index.LLAMA()

# Function to find the most relevant paragraph based on the question
def find_relevant_paragraph(question, text):
    paragraphs = text.split("\n")
    llama.build(paragraphs)
    results = llama.query(question, top_k=1)
    if results:
        most_relevant_paragraph = paragraphs[results[0]['index']]
        return most_relevant_paragraph
    else:
        return text

# Streamlit interface
st.title("Ask My PDF 💾")

# PDF Uploader
uploaded_file = st.file_uploader("Choose a PDF file.", type="pdf")

if uploaded_file is not None:
    try:
        with st.spinner("Reading PDF..."):
            reader = PdfReader(uploaded_file)
            num_pages = len(reader.pages)
            full_text = ""
            for i in range(num_pages):
                page = reader.pages[i]
                full_text += page.extract_text()
            st.session_state.full_text = full_text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# Form for Question
with st.form("Question"):
    question = st.text_input("Question", value="", type="default")
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            with st.spinner("Processing question..."):
                relevant_paragraph = find_relevant_paragraph(question, st.session_state.full_text)
                st.write(relevant_paragraph)
        except Exception as e:
            st.error(f"Error processing question: {e}")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import requests
import PyPDF2
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize environment variables
load_dotenv()

# Initialize session state variables if they don't exist
if 'df' not in st.session_state:
    st.session_state.df = None

if 'prompt_history' not in st.session_state:
    st.session_state.prompt_history = []

# Check and store OpenAI API key
if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
    print("OPENAI_API_KEY is not set")
    exit(1)
else:
    print("OPENAI_API_KEY is set")

# Store API token in session state
st.session_state.openai_key = os.getenv("OPENAI_API_KEY")

# Function to ask the OpenAI chat model
def ask_openai_chat_model(question, context):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4-32k",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{context}"},
            {"role": "user", "content": f"Question: {question}"}
        ]
    }
    headers = {
        "Authorization": f"Bearer {st.session_state.openai_key}"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']

# Function to find the most relevant paragraph based on the question
def find_relevant_paragraph(question, text, num_paragraphs=1):
    paragraphs = re.split('\n\n+', text)
    documents = [question] + paragraphs
    vectorizer = TfidfVectorizer().fit_transform(documents)
    cosine_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:])
    most_similar_paragraph_index = cosine_matrix.argsort()[0][-num_paragraphs:][::-1]
    most_similar_paragraphs = " ".join([paragraphs[i] for i in most_similar_paragraph_index])
    return most_similar_paragraphs

# Streamlit Interface
st.title("Ask My PDF 💾")
st.write("Upload a PDF and ask it questions.")

# File Uploader
if st.session_state.df is None:
    uploaded_file = st.file_uploader("Choose a PDF file.", type=["pdf"])
    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            st.session_state.df = pd.DataFrame({'Text': text.split('\n')})
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# Form for Question
with st.form("Question"):
    question = st.text_input("Question", value="", type="default")
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            with st.spinner():
                extracted_text = " ".join(st.session_state.df['Text'].dropna())
                relevant_paragraph = find_relevant_paragraph(question, extracted_text)
                answer = ask_openai_chat_model(question, relevant_paragraph)
                st.write(answer)
                st.session_state.prompt_history.append(question)
        except Exception as e:
            st.error(f"Error processing question: {e}")

# Display current DataFrame and prompt history
# if st.session_state.df is not None:
#     st.subheader("Current dataframe:")
#     st.write(st.session_state.df)

st.subheader("Prompt history:")
st.write(st.session_state.prompt_history)

# Clear button
if st.button("Clear"):
    st.session_state.prompt_history = []
    st.session_state.df = None
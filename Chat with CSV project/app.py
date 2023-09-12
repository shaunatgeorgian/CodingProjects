import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Initialize environment variables
load_dotenv()

# Check and store OpenAI API key
if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
    print("OPENAI_API_KEY is not set")
    exit(1)
else:
    print("OPENAI_API_KEY is set")

# Initialize session state variables if they don't exist
if 'df' not in st.session_state:
    st.session_state.df = None

if 'prompt_history' not in st.session_state:
    st.session_state.prompt_history = []

# Store API token in session state
st.session_state.openai_key = os.getenv("OPENAI_API_KEY")

# Streamlit Interface
st.title("pandas-ai streamlit interface")
st.write("A demo interface for [PandasAI](https://github.com/gventuri/pandas-ai)")
st.write("Looking for an example *.csv-file?, check [here](https://gist.github.com/netj/8836201).")

# File Uploader
if st.session_state.df is None:
    uploaded_file = st.file_uploader("Choose a CSV file. This should be in long format (one datapoint per row).", type="csv")
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

# Form for Question
with st.form("Question"):
    question = st.text_input("Question", value="", type="default")
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            with st.spinner():
                llm = OpenAI(api_token=st.session_state.openai_key)
                pandas_ai = PandasAI(llm)
                x = pandas_ai.run(st.session_state.df, prompt=question)
                
                fig = plt.gcf()
                if fig.get_axes():
                    st.pyplot(fig)
                st.write(x)
                st.session_state.prompt_history.append(question)
        except Exception as e:
            st.error(f"Error processing question: {e}")

# Display current DataFrame and prompt history
if st.session_state.df is not None:
    st.subheader("Current dataframe:")
    st.write(st.session_state.df)

st.subheader("Prompt history:")
st.write(st.session_state.prompt_history)

# Clear button
if st.button("Clear"):
    st.session_state.prompt_history = []
    st.session_state.df = None

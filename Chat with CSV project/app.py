import pandas as pd
import tempfile
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ... (the rest of your imports and code)

def main():
    # ... (your existing code)

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        # Read the uploaded file into a DataFrame
        df = pd.read_csv(user_csv)

        # Save the DataFrame to a temporary file
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(df.to_csv(index=False).encode('utf-8'))

        user_question = st.text_input("Ask a question about your CSV file:")

        llm = OpenAI(temperature=0)
        
        # Pass the temporary file's path to create_csv_agent()
        agent = create_csv_agent(llm, tfile.name, verbose=True)

        if user_question is not None and user_question != "":
            st.write(f"Your question was: {user_question}")

if __name__ == "__main__":
    main()

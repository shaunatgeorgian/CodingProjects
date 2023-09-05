import pandas as pd
import tempfile
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

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
            with st.spinner(text="In progress..."):
                st.write(f"Your question was: {user_question}")
                try:
                    # This is where we ask the question and get the answer
                    response = agent.run(user_question)
                except Exception as e:
                    response = f"An error occurred: {e}"

                st.write(f"Answer: {response}")

if __name__ == "__main__":
    main()

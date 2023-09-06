import pandas as pd
import tempfile
import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        df = pd.read_csv(user_csv)
        
        # Limiting the DataFrame to first 100 rows to avoid token limit
        df_limited = df.head(100)

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(df_limited.to_csv(index=False).encode('utf-8'))

        user_question = st.text_input("Ask a question about your CSV file:")

        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, tfile.name, verbose=True)

        if user_question is not None and user_question != "":
            with st.spinner(text="In progress..."):
                try:
                    response = agent.run(user_question)
                except Exception as e:
                    response = f"An error occurred: {e}. Try using a shorter question or smaller dataset."
                    
                st.write(f"Answer: {response}")

if __name__ == "__main__":
    main()

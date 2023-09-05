import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv

def main():

    load_dotenv()

    st.set_page_config(page_title="Ask your CSV 📊")
    st.header("Ask your CSV 📊")

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        user_question = st.text_input("Ask a question about your CSV file:")

        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, user_csv, verbose=True)

        if user_question is not None and user_question.question != "":
            response = agent.run(user_question)
            
            st.write(f"Your question was: {user_question}")

if __name__ == "__main__":
    main()
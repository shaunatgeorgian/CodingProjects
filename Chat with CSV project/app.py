# import pandas as pd
# import tempfile
# import streamlit as st
# from langchain.agents import create_csv_agent
# from langchain.llms import OpenAI
# from dotenv import load_dotenv
# import os

# def main():
#     load_dotenv()

#     # Load the OpenAI API key from the environment variable
#     if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
#         print("OPENAI_API_KEY is not set")
#         exit(1)
#     else:
#         print("OPENAI_API_KEY is set")

#     st.set_page_config(page_title="Ask your CSV")
#     st.header("Ask your CSV 📈")

#     # Initialize session state for questions and answers
#     if 'questions' not in st.session_state:
#         st.session_state.questions = []
#     if 'answers' not in st.session_state:
#         st.session_state.answers = []

#     user_csv = st.file_uploader("Upload your CSV file", type="csv")

#     if user_csv is not None:
#         # Read the uploaded file into a DataFrame
#         df = pd.read_csv(user_csv)

#         # Save the DataFrame to a temporary file
#         tfile = tempfile.NamedTemporaryFile(delete=False) 
#         tfile.write(df.to_csv(index=False).encode('utf-8'))


#         llm = OpenAI(temperature=0)
        
#         # Pass the temporary file's path to create_csv_agent()
#         agent = create_csv_agent(llm, tfile.name, verbose=True)

#         user_question = st.text_input("Ask a question about your CSV file:")


#         if user_question:
#             with st.spinner(text="In progress..."):
#                 try:
#                     response = agent.run(user_question)
#                     st.session_state.questions.append(user_question)
#                     st.session_state.answers.append(response)
#                 except Exception as e:
#                     response = f"An error occurred: {e}"
#                     st.session_state.answers.append(response)
            
#             for q, a in zip(st.session_state.questions, st.session_state.answers):
#                 st.write(f"Q: {q}")
#                 st.write(f"A: {a}")

# if __name__ == "__main__":
#     main()

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

    if 'conversation' not in st.session_state:
        st.session_state.conversation = ""

    user_csv = st.file_uploader("Upload your CSV file", type="csv")

    if user_csv is not None:
        df = pd.read_csv(user_csv)
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(df.to_csv(index=False).encode('utf-8'))

        llm = OpenAI(temperature=0)
        agent = create_csv_agent(llm, tfile.name, verbose=True)

        user_question = st.text_input("Ask a question about your CSV file:")

        if user_question:
            with st.spinner(text="In progress..."):
                st.session_state.conversation += f"Q: {user_question}\n"

                try:
                    response = agent.run(st.session_state.conversation)
                    st.session_state.conversation += f"A: {response}\n"
                except Exception as e:
                    response = f"An error occurred: {e}"
                    st.session_state.conversation += f"A: {response}\n"
                
                # Display the conversation history
                st.write(st.session_state.conversation)

if __name__ == "__main__":
    main()

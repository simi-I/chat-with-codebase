import streamlit as st
import utils
import time
import os
local = True
if local:
    from dotenv import load_dotenv
    load_dotenv()
    
st.title("Chat-with-your-codebase")

if local:
    user_key = os.environ.get('OPENAI_API_KEY')
else:
    user_key = st.text_input("Enter your OpenAI key", "")

if user_key:
    os.environ['OPENAI_API_KEY'] = user_key
    
    user_repo = st.text_input("Github link to the public codebase", "https://github.com/simi-I/Chat_with_pdf.git")
    
    if user_repo:
        st.write("You entered:", user_repo)
        
        ##load the Github Repo
        embedder = utils.Embedder(user_repo)
        embedder.clone_repo()
        st.write("Your repo has been cloned")
        
        ##Chunk and Create DB
        st.write("Parsing the content and Embedding it. This may take some time")
        embedder.load_db()
        st.write("Done Loading. Ready to take your Questions")
        
        if "message" not in st.session_state:
            st.session_state.messages = []
            
        #Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
        
        if prompt := st.chat_input("Type your question here"):
            #Add user message to chat history
            st.session_state.messages.append({"role":"user", "content": prompt})
            #Display user message in chat message container 
            with st.chat_message("user"):
                st.markdown(prompt)
            response = embedder.retrieve_results(prompt)
            
            #Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response })
import streamlit as st
from src.whisper_utils import transcribe_audio
from src.chatbot import generate_answer

st.title("Enterprise FAQ Chatbot")

# Sidebar: upload docs or audio
st.sidebar.header("Data ingestion")
uploaded_docs = st.sidebar.file_uploader("Upload PDF/TXT", accept_multiple_files=True)
if st.sidebar.button("Index documents"):
    for doc in uploaded_docs:
        # call your ingestion function here
        pass

st.header("Posez votre question ou déposez un audio")
question = st.text_input("Question")
audio = st.file_uploader("Audio file", type=["mp3","wav"])
if audio is not None:
    text = transcribe_audio(audio)
    st.write("Transcription:", text)
    question = text

if st.button("Envoyer"):
    answer = generate_answer(question, collection_name="company_faq")
    st.success(answer)

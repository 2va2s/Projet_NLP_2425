import streamlit as st
from src.whisper_utils import transcribe_audio
from src.chatbot import generate_answer
from src.ingest import embed_and_store
import os

st.title("Enterprise FAQ Chatbot")

# Sidebar: upload docs or audio
st.sidebar.header("Data ingestion")
uploaded_docs = st.sidebar.file_uploader("Upload PDF/TXT", accept_multiple_files=True)
if st.sidebar.button("Index documents"):
    if uploaded_docs:
        for doc in uploaded_docs:
            # Save the uploaded file into the raw_docs folder
            raw_dir = "data/raw_docs"
            os.makedirs(raw_dir, exist_ok=True)
            raw_path = os.path.join(raw_dir, doc.name)
            with open(raw_path, "wb") as f:
                f.write(doc.read())

            # Call your ingestion function, storing in the 'company_faq' collection
            embed_and_store(raw_path, collection_name="company_faq")

        st.sidebar.success("Documents indexed successfully.")
    else:
        st.sidebar.warning("Please upload at least one document before indexing.")

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

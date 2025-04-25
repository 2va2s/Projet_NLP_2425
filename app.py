import streamlit as st
import tempfile
from src.whisper_utils import transcribe_audio
from src.chatbot import generate_answer
from src.ingest import embed_and_store
import wave
import numpy as np
import os
import io 

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
audio = st.audio_input(
    "🎤 Record your question", 
    label_visibility="visible"
)  # returns UploadedFile (BytesIO) or None :contentReference[oaicite:0]{index=0}


if audio is not None:
    st.session_state.audio_bytes = audio.getvalue() 
    audio = io.BytesIO(st.session_state.audio_bytes)  # Convert to BytesIO for processing
    audio.name = "voice_input.mp3"

    question = transcribe_audio(audio)
    st.write("Transcription :", question)

if st.button("Envoyer"):
    answer = generate_answer(question, collection_name="company_faq")
    st.success(answer)

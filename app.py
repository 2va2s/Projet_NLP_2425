import streamlit as st
st.set_page_config(page_title="FAQ Chatbot", page_icon="💬")


import os
import io
import sys
import tempfile
import wave

from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av

# Ajout des chemins
sys.path.append(os.path.abspath("src"))

from whisper_utils import transcribe_audio
from chatbot import generate_answer
from ingest import embed_and_store
from chroma_index import list_documents, delete_document_chunks

st.title("💬 Enterprise FAQ Chatbot")

# Initialiser l'historique
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Barre latérale - ingestion de documents
st.sidebar.header("📄 Ingestion de documents")
uploaded_docs = st.sidebar.file_uploader("Uploader un PDF ou TXT", accept_multiple_files=True)
if st.sidebar.button("📥 Indexer les documents"):
    if uploaded_docs:
        raw_dir = "data/raw_docs"
        os.makedirs(raw_dir, exist_ok=True)
        for doc in uploaded_docs:
            raw_path = os.path.join(raw_dir, doc.name)
            with open(raw_path, "wb") as f:
                f.write(doc.read())
            embed_and_store(raw_path, collection_name="company_faq")
        st.sidebar.success("Documents indexés avec succès ✅")
    else:
        st.sidebar.warning("Veuillez uploader au moins un document.")

# Barre latérale - gestion des fichiers
st.sidebar.header("🧠 Base de connaissances")
kb_docs = list_documents("company_faq")
selected_doc = st.sidebar.selectbox("Documents indexés", kb_docs)
if st.sidebar.button("🗑️ Supprimer ce document"):
    if selected_doc:
        delete_document_chunks("company_faq", selected_doc)
        st.sidebar.success(f"Supprimé : {selected_doc}")

# Affichage de l'historique
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Saisie vocale via microphone
st.markdown("### 🎤 Posez votre question à l'oral")
webrtc_ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=1024,
    media_stream_constraints={"audio": True, "video": False},
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    sendback_audio=False,
)


if webrtc_ctx.audio_receiver:
    audio_frames = []
    while True:
        try:
            frame = webrtc_ctx.audio_receiver.get_frame(timeout=1)
        except:
            break
        audio_frames.append(frame)

    if audio_frames:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            audio_path = f.name
            with wave.open(f, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                for frame in audio_frames:
                    wf.writeframes(frame.to_ndarray().tobytes())

        with open(audio_path, "rb") as af:
            transcription = transcribe_audio(af)

        with st.chat_message("user"):
            st.markdown(f"*Micro* : {transcription}")
        st.session_state.chat_history.append({"role": "user", "content": transcription})

        answer = generate_answer(transcription, collection_name="company_faq")
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

# Saisie texte classique
prompt = st.chat_input("Posez votre question ici")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    answer = generate_answer(prompt, collection_name="company_faq")
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.chat_history.append({"role": "assistant", "content": answer})

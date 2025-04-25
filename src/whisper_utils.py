import whisper
from openai import OpenAI
from src.config import WHISPER_MODEL_BASE, OPENAI_API_KEY  # on importe depuis src/config.py, qui a déjà load_dotenv()

client = OpenAI(api_key=OPENAI_API_KEY)

# Ensure the model name/path is defined
if WHISPER_MODEL_BASE is None:
    raise EnvironmentError("WHISPER_MODEL_BASE is not set in your .env file")

def transcribe_audio(audio: str) -> str:
    """Transcribe an audio file to text using Whisper."""
    transcription = client.audio.transcriptions.create(
        model=WHISPER_MODEL_BASE,
        file=audio
    )
    return transcription.text
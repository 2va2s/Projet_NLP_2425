import whisper
from src.config import WHISPER_MODEL_BASE  # on importe depuis src/config.py, qui a déjà load_dotenv()

# Ensure the model name/path is defined
if WHISPER_MODEL_BASE is None:
    raise EnvironmentError("WHISPER_MODEL_BASE is not set in your .env file")

# Load the Whisper model specified in .env
model = whisper.load_model(WHISPER_MODEL_BASE)

def transcribe_audio(audio_path: str) -> str:
    """Transcribe an audio file to text using Whisper."""
    result = model.transcribe(audio_path)
    return result["text"]

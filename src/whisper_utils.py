import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_file):
    audio_file.seek(0)
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

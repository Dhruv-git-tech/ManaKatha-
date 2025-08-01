import streamlit as st
import tempfile
import whisper

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def transcribe_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_file.flush()
        model = load_whisper_model()
        result = model.transcribe(tmp_file.name, language="te")
        return result["text"]

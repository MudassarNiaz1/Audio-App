# conda activate G:\AKTI_WORK\Gemini_Audio_App\GEMINI_AUDIO

import os
import tempfile

import google.generativeai as genai
import speech_recognition as sr
import streamlit as st
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    # Existing logic for WAV and FLAC files
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

def summarize_text(text):
    model = genai.GenerativeModel(model_name="gemini-1.5-pro-001")
    response = model.generate_content(
        [
            "Please summarize the following text.",
            text
        ]
    )
    if hasattr(response, 'text'):
        return response.text
    else:
        return "Error: Unable to summarize text."

def save_uploaded_file(uploaded_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            return temp_file.name
    except Exception as e:
        st.error(f"Error Handling uploaded file: {e}")
        return None

# Streamlit interface
st.title("Audio Summarization App")

with st.expander("About this app"):
    st.write("""
This app uses Gemini model to summarize audio files.
Upload your audio file in WAV and MP3 format and get a concise summary of its content.
""")

audio_file = st.file_uploader("Upload Audio File", type=['wav', 'mp3'])
if audio_file is not None:
    audio_path = save_uploaded_file(audio_file)
    st.audio(audio_path)

    if st.button("Summarize Audio"):
        with st.spinner("Transcribing audio..."):
            transcribed_text = transcribe_audio(audio_path)
        with st.spinner("Summarizing..."):
            summary_text = summarize_text(transcribed_text)
            st.info(summary_text)
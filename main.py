import streamlit as st
import torch
import os
import tempfile
from pydub import AudioSegment
from TTS.api import TTS

st.set_page_config(
    page_title="AI Voice Cloning Studio",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ AI Voice Cloning Studio")
st.write("Generate expressive speech using your own cloned voice.")

os.environ["COQUI_TOS_AGREED"] = "1"

device = "cuda" if torch.cuda.is_available() else "cpu"

@st.cache_resource
def load_model():
    st.info("Loading XTTS-v2 voice cloning model...")
    model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    return model

tts = load_model()

MOOD_SETTINGS = {
    "Neutral": {"speed": 1.0, "pitch": 1.0, "energy": 1.0},
    "Happy": {"speed": 1.1, "pitch": 1.2, "energy": 1.2},
    "Sad": {"speed": 0.9, "pitch": 0.8, "energy": 0.8},
    "Angry": {"speed": 1.2, "pitch": 1.1, "energy": 1.5},
    "Calm": {"speed": 0.95, "pitch": 0.9, "energy": 0.9},
    "Excited": {"speed": 1.3, "pitch": 1.3, "energy": 1.4}
}

def process_audio(input_file, mood_params, user_speed):

    with tempfile.TemporaryDirectory() as tmpdir:

        raw_path = os.path.join(tmpdir, "raw.wav")
        output_path = os.path.join(tmpdir, "generated.wav")

        with open(raw_path, "wb") as f:
            f.write(input_file.read())

        tts.tts_to_file(
            text=user_text,
            speaker_wav=raw_path,
            language="en",
            speed=mood_params["speed"],
            file_path=output_path
        )

        audio = AudioSegment.from_wav(output_path)

        audio = audio + (mood_params["energy"] * 5)

        if mood_params["pitch"] != 1.0:
            audio = audio.speedup(playback_speed=mood_params["pitch"])

        audio = audio.speedup(playback_speed=user_speed)

        final_wav = os.path.join(tmpdir, "final.wav")
        final_mp3 = os.path.join(tmpdir, "final.mp3")
        final_ogg = os.path.join(tmpdir, "final.ogg")

        audio.export(final_wav, format="wav")
        audio.export(final_mp3, format="mp3")
        audio.export(final_ogg, format="ogg")

        return final_wav, final_mp3, final_ogg


st.subheader("🎤 Upload Voice Sample")

voice_file = st.file_uploader(
    "Upload WAV voice sample (recommended 5-10 seconds)",
    type=["wav"]
)

if voice_file:
    st.audio(voice_file)

st.subheader("🎭 Select Emotion")

mood = st.selectbox(
    "Choose voice mood",
    list(MOOD_SETTINGS.keys())
)

st.subheader("⚡ Speech Speed")

speech_speed = st.slider(
    "Speech speed",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

st.subheader("✍️ Enter Text")

user_text = st.text_area(
    "Text to synthesize",
    "Hello, this is my AI generated voice."
)

if st.button("🎙️ Generate Voice"):

    if voice_file is None:
        st.error("Please upload a voice sample.")
        st.stop()

    if len(user_text.strip()) == 0:
        st.error("Please enter text.")
        st.stop()

    mood_params = MOOD_SETTINGS[mood]

    with st.spinner("Generating cloned voice..."):

        wav, mp3, ogg = process_audio(
            voice_file,
            mood_params,
            speech_speed
        )

    st.success("Voice generation complete!")

    st.audio(wav)

    col1, col2, col3 = st.columns(3)

    with col1:
        with open(wav, "rb") as f:
            st.download_button(
                "Download WAV",
                f,
                file_name="cloned_voice.wav"
            )

    with col2:
        with open(mp3, "rb") as f:
            st.download_button(
                "Download MP3",
                f,
                file_name="cloned_voice.mp3"
            )

    with col3:
        with open(ogg, "rb") as f:
            st.download_button(
                "Download OGG",
                f,
                file_name="cloned_voice.ogg"
            )

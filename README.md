# AI Voice Cloning Application
AI-powered voice cloning system that generates expressive speech from a short voice sample using Coqui XTTS-v2 and Streamlit.
Overview

The AI Voice Cloning Application is a machine learning–based system that generates speech using a cloned voice from a short audio sample. By uploading a voice recording, users can synthesize natural-sounding speech that closely resembles the original speaker.

The application also allows users to customize the generated speech by adjusting mood, speed, and style, making the output more expressive and realistic. This project demonstrates the capabilities of modern AI-driven text-to-speech (TTS) systems and provides an interactive platform for experimenting with voice synthesis.

Features
Upload a short WAV voice sample for cloning.
Generate speech that mimics the uploaded voice.
Select different emotional tones such as:
Neutral
Happy
Sad
Angry
Calm
Excited
Adjust speech speed to control how fast or slow the generated voice sounds.
Enter custom text input to generate speech.
Download generated audio in multiple formats (WAV, MP3, OGG).
Record audio directly within the application.
Technology Stack

The application integrates machine learning models, audio processing libraries, and web technologies to deliver a smooth user experience.

Technology	Purpose
Streamlit	Provides the web interface and handles user interactions
PyTorch	Runs the deep learning model and manages GPU acceleration
Coqui XTTS-v2	Multilingual text-to-speech model used for voice cloning
Pydub	Performs post-processing such as pitch, speed, and energy adjustments
Streamlit WebRTC	Enables direct audio recording from the browser
How the System Works
1. Model Initialization

The application checks whether a GPU is available using:

torch.cuda.is_available()

The Coqui XTTS-v2 model is then loaded to perform voice cloning and speech synthesis.

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

This model generates speech that closely matches the characteristics of the uploaded voice sample.

2. Voice Sample Processing

Users upload a WAV audio file containing a short sample of their voice.

The application extracts key voice characteristics such as:

Tone
Pitch
Speaking style

These characteristics are used as a reference during speech synthesis.

3. Speech Generation

Users enter text and select a mood for the generated speech.

Each mood has predefined parameters controlling speed, pitch, and energy.

Example configuration:

mood_settings = {
    "Neutral": {"speed": 1.0, "pitch": 1.0, "energy": 1.0},
    "Happy": {"speed": 1.1, "pitch": 1.2, "energy": 1.2},
    "Sad": {"speed": 0.9, "pitch": 0.8, "energy": 0.8},
    "Angry": {"speed": 1.2, "pitch": 1.1, "energy": 1.5},
    "Calm": {"speed": 0.95, "pitch": 0.9, "energy": 0.9},
    "Excited": {"speed": 1.3, "pitch": 1.3, "energy": 1.4}
}

These parameters allow the generated speech to sound more expressive and dynamic.

4. Audio Synthesis

The text is converted into speech using the cloned voice:

tts.tts_to_file(
    text=text,
    speaker_wav=audio_path,
    language="en",
    speed=mood_params["speed"],
    file_path=output_wav
)
5. Post-Processing

After speech generation, Pydub is used to apply additional enhancements such as:

Pitch adjustments
Energy modifications
Speed refinement

This improves the overall quality and naturalness of the generated audio.

6. Output & Download

The generated speech can be:

Played directly within the application
Downloaded in multiple formats:
WAV
MP3
OGG
Getting Started

Follow these steps to use the application:

Upload or record a short voice sample.
Select a mood and adjust the speech speed.
Enter the text you want the cloned voice to speak.
Click Generate to produce the speech.
Listen to the output and download the audio file if needed.
Project Goal

This project was developed to demonstrate the capabilities of AI-based voice cloning and speech synthesis while maintaining simplicity and accessibility. It provides a practical implementation of modern text-to-speech technology and highlights how machine learning can be used to create realistic voice generation systems.

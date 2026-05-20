import os
import tempfile
import logging
from elevenlabs.client import ElevenLabs

logger = logging.getLogger("Tina")

client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))


def play_audio(file_path: str):
    os.startfile(file_path)


def speak(text: str):
    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=os.getenv("TINA_VOICE_ID"),
            model_id="eleven_multilingual_v2",
            text=text
        )

        # 🔥 Convert generator → bytes
        audio_bytes = b"".join(audio_stream)

        # Save to file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(audio_bytes)
            file_path = f.name

        play_audio(file_path)

    except Exception as e:
        logger.error(f"TTS error: {e}")
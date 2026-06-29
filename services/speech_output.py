# services/speech_output.py

import asyncio
import threading
import queue
import logging
import tempfile
import os

import edge_tts
import sounddevice as sd
import soundfile as sf

logger = logging.getLogger("Tina")

# =====================================================
# CONFIG
# =====================================================

# Full list: run `edge-tts --list-voices` in terminal
# Top natural English voices:
# en-US-JennyNeural        — warm, conversational (recommended)
# en-US-AriaNeural         — clear, professional
# en-US-SaraNeural         — friendly, bright
# en-GB-SoniaNeural        — British female
# en-AU-NatashaNeural      — Australian female

VOICE = "en-US-JennyNeural"
RATE  = "+0%"    # speed: "-10%" slower, "+10%" faster
PITCH = "+0Hz"   # pitch: "-5Hz" lower, "+5Hz" higher


# =====================================================
# SPEECH OUTPUT (Edge TTS)
# =====================================================

class SpeechOutput:

    def __init__(self):
        self._queue = queue.Queue()
        self.capture = None  # set to SpeechCapture after init

        self._thread = threading.Thread(
            target=self._run_loop,
            daemon=True
        )
        self._thread.start()
        logger.info("🔊 Speech output ready (Edge TTS — JennyNeural).")

    # --------------------------------------------------
    # DEDICATED SPEECH THREAD
    # --------------------------------------------------

    def _run_loop(self):
        """
        Runs forever on its own thread.
        Picks text from queue, synthesizes, plays.
        """
        # Each thread needs its own event loop for edge_tts
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        while True:
            text = self._queue.get()

            if text is None:  # shutdown signal
                break

            try:
                if self.capture:
                    self.capture.mute()

                logger.info(f"Speaking: {text[:60]}...")
                loop.run_until_complete(self._synthesize_and_play(text))

            except Exception as e:
                logger.error(f"Speech error: {e}", exc_info=True)

            finally:
                if self.capture:
                    self.capture.unmute()

            self._queue.task_done()

        loop.close()

    # --------------------------------------------------
    # SYNTHESIZE + PLAY
    # --------------------------------------------------

    async def _synthesize_and_play(self, text: str):
        """
        Generate audio with Edge TTS and play through speakers.
        Uses a temp file — Edge TTS streams mp3, soundfile reads it.
        """

        tmp_path = None

        try:
            # Write to temp mp3 file
            with tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False
            ) as tmp:
                tmp_path = tmp.name

            communicate = edge_tts.Communicate(
                text=text,
                voice=VOICE,
                rate=RATE,
                pitch=PITCH
            )
            await communicate.save(tmp_path)

            # Read and play
            data, samplerate = sf.read(tmp_path, dtype="float32")
            sd.play(data, samplerate=samplerate)
            sd.wait()

        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    # --------------------------------------------------
    # PUBLIC API — safe from any thread or async context
    # --------------------------------------------------

    def speak(self, text: str):
        """Queue text for speaking. Returns immediately."""
        if text and text.strip():
            self._queue.put(text.strip())

    def speak_sync(self, text: str):
        """Block until speech finishes."""
        if text and text.strip():
            self._queue.put(text.strip())
            self._queue.join()

    def stop(self):
        self._queue.put(None)
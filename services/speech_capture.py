# services/speech_capture.py

import whisper
import sounddevice as sd
import numpy as np
import threading
import queue
import logging

logger = logging.getLogger("Tina")

# =====================================================
# CONFIG
# =====================================================

SAMPLE_RATE       = 16000
CHUNK_DURATION    = 0.3   # smaller chunks = less overflow
SILENCE_THRESHOLD = 0.01
SILENCE_TIMEOUT   = 1.0   # seconds of silence before processing
MIN_SPEECH_DURATION = 0.4


# =====================================================
# SPEECH CAPTURE
# =====================================================

class SpeechCapture:

    def __init__(self, model_size="tiny", on_transcription=None):
        self.model_size = model_size
        self.model = None

        self.on_transcription = on_transcription
        self.running = False
        self.muted = False
        self._transcribing = False  # prevents overlap

        # Larger maxsize so overflow happens less
        self._audio_queue = queue.Queue(maxsize=200)

        self._buffer = []
        self._silence_counter = 0
        self._speaking = False

    # --------------------------------------------------
    # LAZY MODEL LOAD
    # --------------------------------------------------

    def _ensure_model(self):
        if self.model is None:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded.")

    # --------------------------------------------------
    # MUTE CONTROL
    # --------------------------------------------------

    def mute(self):
        self.muted = True
        self._buffer = []
        self._speaking = False
        self._silence_counter = 0
        # Drain queue
        while not self._audio_queue.empty():
            try:
                self._audio_queue.get_nowait()
            except queue.Empty:
                break

    def unmute(self):
        self.muted = False

    # --------------------------------------------------
    # START / STOP
    # --------------------------------------------------

    def start(self):
        self.running = True
        threading.Thread(target=self._listen_loop, daemon=True).start()
        threading.Thread(target=self._process_loop, daemon=True).start()
        logger.info("🎙️ Speech capture started.")

    def stop(self):
        self.running = False
        logger.info("🎙️ Speech capture stopped.")

    # --------------------------------------------------
    # AUDIO CAPTURE LOOP
    # --------------------------------------------------

    def _listen_loop(self):

        chunk_size = int(SAMPLE_RATE * CHUNK_DURATION)

        def callback(indata, frames, time, status):
            if status:
                # Only log overflow once in a while, not every chunk
                if 'overflow' not in str(status).lower() or \
                   np.random.random() < 0.05:
                    logger.warning(f"Audio status: {status}")
            if not self.muted:
                try:
                    self._audio_queue.put_nowait(indata[:, 0].copy())
                except queue.Full:
                    pass  # drop chunk silently if queue full

        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=chunk_size,
            latency='low',         # request low latency
            callback=callback
        ):
            while self.running:
                sd.sleep(50)

    # --------------------------------------------------
    # SPEECH DETECTION LOOP (never blocks on transcription)
    # --------------------------------------------------

    def _process_loop(self):

        silence_chunks_needed = int(SILENCE_TIMEOUT / CHUNK_DURATION)

        while self.running:

            try:
                chunk = self._audio_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if self.muted:
                continue

            amplitude = np.abs(chunk).mean()
            is_speech = amplitude > SILENCE_THRESHOLD

            if is_speech:
                self._speaking = True
                self._silence_counter = 0
                self._buffer.append(chunk)

            elif self._speaking:
                self._silence_counter += 1
                self._buffer.append(chunk)

                if self._silence_counter >= silence_chunks_needed:

                    # Only transcribe if not already transcribing
                    if not self._transcribing:
                        audio_snapshot = list(self._buffer)
                        threading.Thread(
                            target=self._transcribe,
                            args=(audio_snapshot,),
                            daemon=True
                        ).start()

                    self._buffer = []
                    self._speaking = False
                    self._silence_counter = 0

    # --------------------------------------------------
    # TRANSCRIBE (runs on its own thread, never blocks)
    # --------------------------------------------------

    def _transcribe(self, buffer):

        self._transcribing = True

        try:
            audio = np.concatenate(buffer)
            duration = len(audio) / SAMPLE_RATE

            if duration < MIN_SPEECH_DURATION:
                return

            self._ensure_model()

            result = self.model.transcribe(
                audio,
                language="en",
                fp16=False,
                condition_on_previous_text=False  # faster
            )

            text = result["text"].strip()

            if text and self.on_transcription:
                logger.info(f"Transcribed: {text}")
                self.on_transcription(text)

        except Exception as e:
            logger.error(f"Transcription error: {e}", exc_info=True)

        finally:
            self._transcribing = False
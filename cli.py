import logging
import asyncio
import sys

from core.orchestrator import process
from database.db import init_db
from core.reminder_scheduler import reminder_loop
from services.speech_output import SpeechOutput
from services.speech_capture import SpeechCapture

# =====================================================
# MODE FLAG
# python cli.py          → text mode (default)
# python cli.py --voice  → full voice mode
# =====================================================

VOICE_MODE = "--voice" in sys.argv

# =====================================================
# SHARED INSTANCES
# =====================================================

tts = SpeechOutput()


# =====================================================
# CORE INPUT HANDLER (shared by both modes)
# =====================================================

async def handle_input(user_input: str, logger):

    user_input = user_input.strip()

    if not user_input:
        return True

    if user_input.lower() in ["exit", "quit"]:
        print("Tina: Goodbye 👋")
        tts.speak("Goodbye!")
        return False

    result = await process(user_input)

    if isinstance(result, dict):
        reply = result.get("reply", "")
        if result.get("type") == "action":
            print(f"Tina (action): {reply}\n")
        else:
            print(f"Tina: {reply}\n")
        if reply:
            tts.speak(reply)
    else:
        print(f"Tina: {result}\n")
        tts.speak(str(result))

    return True


# =====================================================
# TEXT MODE LOOP
# =====================================================

async def text_loop(logger):

    print("\n🤖 Tina AI CLI (Ollama Powered)")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = await asyncio.to_thread(input, "You: ")
            keep_going = await handle_input(user_input, logger)
            if not keep_going:
                break

        except KeyboardInterrupt:
            print("\nTina: Interrupted 👋")
            tts.speak("Interrupted. Goodbye!")
            break

        except Exception as e:
            logger.error(f"CLI Error: {e}")
            print("Tina: Something went wrong.\n")


# =====================================================
# VOICE MODE LOOP
# =====================================================

async def voice_loop(logger):

    print("\n🎙️  Tina AI (Voice Mode)")
    print("Speak to Tina. Say 'exit' or 'quit' to stop.\n")

    current_loop = asyncio.get_event_loop()
    stop_event = asyncio.Event()

    capture = SpeechCapture(
        model_size="base",
        on_transcription=None  # set below
    )

    # ── WIRE mute/unmute so TTS silences the mic while speaking ──
    tts.capture = capture

    def on_speech(text):
        print(f"You: {text}")

        async def _handle():
            keep_going = await handle_input(text, logger)
            if not keep_going:
                stop_event.set()

        asyncio.run_coroutine_threadsafe(_handle(), current_loop)

    capture.on_transcription = on_speech
    capture.start()

    tts.speak("Voice mode active. I'm listening.")

    try:
        await stop_event.wait()
    except KeyboardInterrupt:
        print("\nTina: Interrupted 👋")
        tts.speak("Interrupted. Goodbye!")
    finally:
        capture.stop()


# =====================================================
# SYSTEM BOOTSTRAP
# =====================================================

async def main():

    init_db()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Tina")
    logger.info("Starting Tina system...")

    asyncio.create_task(reminder_loop())

    if VOICE_MODE:
        await voice_loop(logger)
    else:
        await text_loop(logger)


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    asyncio.run(main())
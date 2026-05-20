import os
from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
TINA_VOICE_ID = os.getenv("TINA_VOICE_ID")
TTS_MODEL = os.getenv("TTS_MODEL", "eleven_flash_v2_5")

#SECOND OPTION VOICE ID ="zGjIP4SZlMnY9m93k97r"
#THIRD OPTION VOICE ID = "OY65OHHFELVut7v2H" HOPE NATURAL.Tbf
# tools/system/screen_record.py

import subprocess


def open_screen_recording():

    try:

        subprocess.Popen(
            "explorer ms-gamingoverlay:",
            shell=True
        )

        return {
            "success": True,
            "message": "Opening screen recording tools."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
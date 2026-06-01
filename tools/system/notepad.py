# tools/system/notepad.py

import subprocess


def open_notepad():

    try:

        subprocess.Popen("notepad")

        return {
            "success": True,
            "message": "Opening Notepad."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
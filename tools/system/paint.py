# tools/system/paint.py

import subprocess


def open_paint():

    try:

        subprocess.Popen("mspaint")

        return {
            "success": True,
            "message": "Opening Paint."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
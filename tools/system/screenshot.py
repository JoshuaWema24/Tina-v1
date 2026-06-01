# tools/system/screenshots.py

import subprocess


def open_screenshot_tool():

    try:

        subprocess.Popen(
            "explorer ms-screenclip:",
            shell=True
        )

        return {
            "success": True,
            "message": "Opening screenshot tool."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
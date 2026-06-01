# tools/system/screenshots_folder.py

import subprocess
from pathlib import Path


def open_screenshots_folder():

    try:

        path = (
            Path.home()
            / "Pictures"
            / "Screenshots"
        )

        if not path.exists():

            return {
                "success": False,
                "message":
                    "Screenshots folder not found."
            }

        subprocess.Popen(
            f'explorer "{path}"'
        )

        return {
            "success": True,
            "message":
                "Opening screenshots folder."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
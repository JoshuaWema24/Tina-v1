import subprocess
from pathlib import Path


def find_chrome():

    paths = [
        Path(
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        ),
        Path(
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        )
    ]

    for path in paths:

        if path.exists():
            return str(path)

    return None


def open_chrome():

    chrome = find_chrome()

    if not chrome:

        return {
            "success": False,
            "message": "Chrome not found."
        }

    subprocess.Popen(chrome)

    return {
        "success": True,
        "message": "Opening Chrome."
    }
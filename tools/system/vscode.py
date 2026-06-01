# tools/system/vscode.py

import subprocess
from pathlib import Path


def find_vscode():
    """
    Attempts to locate VS Code.
    """

    paths = [

        Path(
            r"C:\Users\HP\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        ),

        Path(
            r"C:\Program Files\Microsoft VS Code\Code.exe"
        ),

        Path(
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe"
        ),
    ]

    for path in paths:

        if path.exists():
            return str(path)

    return None


def open_vscode():

    try:

        vscode = find_vscode()

        if not vscode:

            return {
                "success": False,
                "message": "Visual Studio Code was not found."
            }

        subprocess.Popen(vscode)

        return {
            "success": True,
            "message": "Opening Visual Studio Code."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
# tools/system/explorer.py

import subprocess
from pathlib import Path
import os


# =====================================================
# COMMON USER FOLDERS MAP
# =====================================================

KNOWN_FOLDERS = {

    "downloads": Path.home() / "Downloads",

    "documents": Path.home() / "Documents",

    "desktop": Path.home() / "Desktop",

    "pictures": Path.home() / "Pictures",

    "music": Path.home() / "Music",

    "videos": Path.home() / "Videos",
}


# =====================================================
# OPEN EXPLORER
# =====================================================

def open_explorer(path=None):

    try:

        # ---------------------------------
        # CASE 1: No path → open default explorer
        # ---------------------------------
        if not path:

            subprocess.Popen("explorer")

            return {
                "success": True,
                "message": "Opening File Explorer."
            }

        # ---------------------------------
        # Normalize input
        # ---------------------------------
        raw = str(path).lower().strip()

        # ---------------------------------
        # CASE 2: Known folders (semantic)
        # ---------------------------------
        if raw in KNOWN_FOLDERS:

            folder_path = KNOWN_FOLDERS[raw]

            subprocess.Popen(f'explorer "{folder_path}"')

            return {
                "success": True,
                "message": f"Opening {raw.title()}."
            }

        # ---------------------------------
        # CASE 3: "my tina project folder" style
        # ---------------------------------
        if "tina" in raw and "project" in raw:

            project_path = Path(
                r"C:\Users\HP\Documents\projects\Tina v1"
            )

            if project_path.exists():

                subprocess.Popen(f'explorer "{project_path}"')

                return {
                    "success": True,
                    "message": "Opening Tina project folder."
                }

            return {
                "success": False,
                "message": "Tina project folder not found."
            }

        # ---------------------------------
        # CASE 4: Direct filesystem path
        # ---------------------------------
        folder = Path(path)

        if folder.exists():

            subprocess.Popen(f'explorer "{folder}"')

            return {
                "success": True,
                "message": f"Opening {folder.name}."
            }

        # ---------------------------------
        # CASE 5: Unknown folder
        # ---------------------------------
        return {
            "success": False,
            "message": f"I couldn't find: {path}"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
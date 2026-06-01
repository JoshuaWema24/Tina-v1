# tools/system/calculator.py

import subprocess


def open_calculator():

    try:

        subprocess.Popen("calc")

        return {
            "success": True,
            "message": "Opening Calculator."
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }
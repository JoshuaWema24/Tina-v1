# tools/registry.py

# =====================================================
# SYSTEM TOOLS
# =====================================================

from tools.system.chrome import open_chrome
from tools.system.calculator import open_calculator
from tools.system.notepad import open_notepad
from tools.system.paint import open_paint
from tools.system.screenshot import open_screenshot_tool
from tools.system.screen_record import open_screen_recording
from tools.system.screenshots_folder import open_screenshots_folder
from tools.system.vscode import open_vscode
from tools.system.explorer import open_explorer

# =====================================================
# TOOL REGISTRY
# =====================================================

TOOLS = {

    # ---------------------------------
    # Browser
    # ---------------------------------

    "open_chrome": open_chrome,

    # ---------------------------------
    # Productivity
    # ---------------------------------

    "open_calculator": open_calculator,

    "open_notepad": open_notepad,

    # ---------------------------------
    # Creative
    # ---------------------------------

    "open_paint": open_paint,

    # ---------------------------------
    # Screenshots
    # ---------------------------------

    "open_screenshot_tool":
        open_screenshot_tool,

    "open_screen_recording":
        open_screen_recording,

    "open_screenshots_folder":
        open_screenshots_folder,

        "open_vscode": open_vscode,
        "open_explorer": open_explorer,
}


# =====================================================
# REGISTRY HELPERS
# =====================================================

def get_tool(tool_name):
    """
    Returns tool function or None.
    """

    return TOOLS.get(tool_name)


def has_tool(tool_name):
    """
    Check if tool exists.
    """

    return tool_name in TOOLS


def get_all_tools():
    """
    Returns all registered tool names.
    """

    return list(TOOLS.keys())


def count_tools():
    """
    Returns number of registered tools.
    """

    return len(TOOLS)
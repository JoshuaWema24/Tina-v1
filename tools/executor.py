# tools/executor.py

import logging

from tools.registry import TOOLS

logger = logging.getLogger("Tina")


# =====================================================
# TOOL EXECUTOR
# =====================================================

def execute(tool_name: str, **kwargs):
    """
    Executes a registered tool.

    Example:

    execute("open_chrome")

    execute(
        "create_reminder",
        text="Meeting at 5 PM"
    )
    """

    tool = TOOLS.get(tool_name)

    if not tool:

        logger.warning(
            f"Unknown tool requested: {tool_name}"
        )

        return {
            "success": False,
            "message": (
                f"Unknown tool: {tool_name}"
            ),
            "data": None
        }

    try:

        logger.info(
            f"Executing tool: {tool_name}"
        )

        result = tool(**kwargs)

        # --------------------------------
        # Normalize return values
        # --------------------------------

        if isinstance(result, dict):

            return {
                "success": result.get(
                    "success",
                    True
                ),
                "message": result.get(
                    "message",
                    ""
                ),
                "data": result.get(
                    "data",
                    None
                )
            }

        # --------------------------------
        # String return
        # --------------------------------

        if isinstance(result, str):

            return {
                "success": True,
                "message": result,
                "data": None
            }

        # --------------------------------
        # Empty return
        # --------------------------------

        return {
            "success": True,
            "message": (
                f"{tool_name} executed."
            ),
            "data": result
        }

    except Exception as e:

        logger.error(
            f"Tool execution error: {e}",
            exc_info=True
        )

        return {
            "success": False,
            "message": str(e),
            "data": None
        }


# =====================================================
# CHECK TOOL EXISTS
# =====================================================

def tool_exists(tool_name: str) -> bool:
    """
    Returns True if tool exists.
    """

    return tool_name in TOOLS


# =====================================================
# LIST TOOLS
# =====================================================

def list_tools():
    """
    Returns all registered tools.
    """

    return list(TOOLS.keys())
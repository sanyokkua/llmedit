import logging
import os
from pathlib import Path

from theme.colors import COLORS

logger = logging.getLogger(__name__)


def substitute_vars(qss: str, variables: dict) -> str:
    """
    Substitute template variables in QSS string with their values.

    Args:
        qss: The QSS template string containing variables in {{name}} format.
        variables: Dictionary mapping variable names to their replacement values.

    Returns:
        QSS string with all variables replaced by their corresponding values.

    Notes:
        Performs simple string replacement for variables enclosed in double braces.
    """
    for name, value in variables.items():
        qss = qss.replace("{{" + name + "}}", value)
    return qss


def load_stylesheet(app_root: Path) -> str:
    """
    Load and process the application stylesheet.

    Args:
        app_root: Path to the application root directory.

    Returns:
        Processed stylesheet string, or empty string if loading fails.

    Notes:
        Loads QSS template from data/themes/theme.qss, substitutes color variables
        from the COLORS dictionary, and returns the final style string.
        Logs warnings if a file is missing and errors if reading fails.
    """
    theme_path = app_root / "data" / "themes" / "theme.qss"
    if not os.path.exists(theme_path):
        logger.warning("Theme file not found at %s", theme_path)
        return ""
    try:
        with open(theme_path, "r") as f:
            qss_template = f.read()
        style = substitute_vars(qss_template, COLORS)
        logger.debug("Loaded stylesheet: %s", style)
        return style
    except Exception as e:
        logger.error("Failed to load stylesheet: %s", e, exc_info=True)
        return ""

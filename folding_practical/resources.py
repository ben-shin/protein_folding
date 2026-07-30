"""Helpers for files bundled with the desktop application."""

from __future__ import annotations

import sys
from pathlib import Path
import tkinter as tk


def resource_path(*parts: str) -> Path:
    """Return a path that works in source and PyInstaller builds."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root).joinpath(*parts)
    return Path(__file__).resolve().parents[1].joinpath(*parts)


def set_window_icon(window: tk.Misc) -> None:
    """Set the application icon when the bundled image is available."""
    icon_path = resource_path("assets", "app_icon.png")
    if not icon_path.exists():
        return
    try:
        icon = tk.PhotoImage(file=str(icon_path))
        window.iconphoto(True, icon)
        window._pfp_icon = icon
    except tk.TclError:
        return

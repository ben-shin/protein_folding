"""Build a dependency-free portable desktop package with PyInstaller."""

from __future__ import annotations

import os
import platform
import shutil
import sys
from pathlib import Path

import PyInstaller.__main__


APP_NAME = "ProteinFoldingPractical"
DISPLAY_NAME = "Protein Folding Practical"
BUNDLE_ID = "io.github.ben-shin.proteinfoldingpractical"
ROOT = Path(__file__).resolve().parent


def _clean() -> None:
    for folder in (ROOT / "build", ROOT / "dist"):
        if folder.exists():
            shutil.rmtree(folder)


def _write_start_here() -> None:
    system = platform.system()
    if system == "Darwin":
        destination = ROOT / "dist" / "START_HERE.txt"
        launch_text = "Double-click Protein Folding Practical.app."
    else:
        destination = ROOT / "dist" / APP_NAME / "START_HERE.txt"
        launch_text = (
            f"Double-click {APP_NAME}.exe."
            if system == "Windows"
            else f"Run ./{APP_NAME}."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        "Protein Folding Practical\n\n"
        f"{launch_text}\n"
        "Python, Conda, and the scientific packages are already included.\n\n"
        "The application is unsigned. Windows SmartScreen or macOS Gatekeeper may "
        "show a warning the first time it opens.\n",
        encoding="utf-8",
    )


def main() -> None:
    _clean()
    icon = ROOT / "assets" / "app_icon.png"
    data_separator = ";" if platform.system() == "Windows" else ":"

    args = [
        str(ROOT / "run_app.py"),
        "--name",
        APP_NAME,
        "--onedir",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--noupx",
        "--contents-directory",
        "_internal",
        "--distpath",
        str(ROOT / "dist"),
        "--workpath",
        str(ROOT / "build"),
        "--specpath",
        str(ROOT / "build"),
        "--add-data",
        f"{ROOT / 'assets'}{data_separator}assets",
        "--hidden-import",
        "matplotlib.backends.backend_tkagg",
        "--hidden-import",
        "scipy.optimize",
        "--collect-data",
        "matplotlib",
        "--exclude-module",
        "pytest",
        "--exclude-module",
        "IPython",
        "--icon",
        str(icon),
    ]

    if platform.system() == "Darwin":
        args.extend(["--osx-bundle-identifier", BUNDLE_ID])

    print(f"Building {DISPLAY_NAME} for {platform.system()} {platform.machine()}...")
    PyInstaller.__main__.run(args)
    _write_start_here()

    if platform.system() == "Darwin":
        output = ROOT / "dist" / f"{APP_NAME}.app"
    else:
        output = ROOT / "dist" / APP_NAME

    if not output.exists():
        raise RuntimeError(f"Build finished but {output} was not created")
    print(f"Portable build created at {output}")


if __name__ == "__main__":
    main()

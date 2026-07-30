#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install -r portable_build_requirements.txt
python build_portable.py

./dist/ProteinFoldingPractical.app/Contents/MacOS/ProteinFoldingPractical --self-test

echo "Build ready in dist/ProteinFoldingPractical.app"

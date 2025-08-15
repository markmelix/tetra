#!/usr/bin/env bash
set -e

if ! command -v python &> /dev/null; then
    echo "Error: python command not found. Please install Python before running this script."
    exit 1
fi

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

echo "Installing dependencies..."
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt pyinstaller

echo "Building executable with PyInstaller..."
venv/bin/pyinstaller \
    --onefile \
    --noconsole \
    --paths src/modules \
    --hidden-import charset_normalizer \
    --hidden-import PyQt5.QtPrintSupport \
    --workpath target/linux/build \
    --distpath target/linux/dist \
    --specpath target/linux \
    src/main.py

echo "Build completed successfully!"


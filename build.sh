#!/usr/bin/bash
venv/bin/pyinstaller --onefile --noconsole --paths src/modules --hidden-import charset_normalizer  --hidden-import PyQt5.QtPrintSupport src/main.py

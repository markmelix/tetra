PYTHON ?= python
VENV_DIR := venv
PIP := $(VENV_DIR)/bin/pip
PYINSTALLER := $(VENV_DIR)/bin/pyinstaller

SRC := src/main.py
REQ := requirements.txt

PYINSTALLER_FLAGS := \
	--onefile \
	--noconsole \
	--paths src/modules \
	--hidden-import charset_normalizer \
	--hidden-import PyQt5.QtPrintSupport \
	--workpath target/linux/build \
	--distpath target/linux/dist \
	--specpath target/linux

.PHONY: all venv install build clean

all: build

venv:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "Error: python command not found."; exit 1; }
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi

install: venv
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r $(REQ) pyinstaller

build: install
	@echo "Building executable with PyInstaller..."
	$(PYINSTALLER) $(PYINSTALLER_FLAGS) $(SRC)
	@echo "Build completed successfully!"
	@echo "Tetra binary should be located at target/linux/dist directory."

clean:
	rm -rf $(VENV_DIR) target/linux

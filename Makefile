.PHONY: all install run build clean

# Python executable
PYTHON = python3
PIP = pip3

all: run

install:
	$(PIP) install -r requirements.txt
	$(PIP) install pyinstaller

run:
	$(PYTHON) run.py

build:
	pyinstaller EmojiPad.spec

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf __pycache__/
	rm -rf src/emojipad/__pycache__/
	rm -rf src/emojipad/core/__pycache__/
	rm -rf src/emojipad/ui/__pycache__/
	rm -f EmojiPad.spec.bak

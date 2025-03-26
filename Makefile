# Makefile for Conway's Game of Life

# Basic variables
PYTHON = python3
MAIN_FILE = main.py
PROJECT_NAME = JeudelaVie
SRC_DIR = src
TEST_DIR = tests
VENV_DIR = venv
VENV_PYTHON = $(VENV_DIR)/bin/python
VENV_PIP = $(VENV_DIR)/bin/pip
VENV_PYTEST = $(VENV_DIR)/bin/pytest

# Default target
all: help

# Targets
.PHONY: all run install clean test help venv check-venv

help:
	@echo "Conway's Game of Life"
	@echo "===================="
	@echo "Available commands:"
	@echo "  make run       - Run the Game of Life simulation"
	@echo "  make install   - Create virtual environment and install required dependencies"
	@echo "  make clean     - Remove Python cache files and virtual environment"
	@echo "  make test      - Run the test suite"
	@echo "  make help      - Show this help message"
	@echo "  make venv      - Create virtual environment only"

# Create virtual environment
venv:
	test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)

# Install dependencies
install: venv
	$(VENV_PIP) install -r requirements.txt

# Check if virtual environment exists
check-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment not found. Creating..."; \
		make venv; \
		$(VENV_PIP) install -r requirements.txt; \
	fi

# Run the game
run: check-venv
	$(VENV_PYTHON) $(MAIN_FILE)

# Clean Python cache files and virtual environment
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf $(VENV_DIR)

# Run tests
test: check-venv
	$(VENV_PYTHON) -m pytest $(TEST_DIR) -v

#!/bin/bash

# Check if the virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating venv: .venv"
    python3 -m venv .venv
fi

# Activate the virtual environment
echo "Setting up venv"
source .venv/bin/activate

# Check if requirements.txt exists and install dependencies
echo "Installing requirements"
pip install -r requirements.txt

echo "Virtual Environment setup complete"

# Run FastApi Orchestrator (dev)
echo "Starting Orchestrator Server, use 'Ctrl + C' to close"
fastapi run orchestrator.py --port 8000
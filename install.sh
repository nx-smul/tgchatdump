#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Please install Python3 and try again."
    exit
fi

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install telethon

echo "Installation complete. Run your script with the following command:"
echo "source venv/bin/activate && python your_script.py"

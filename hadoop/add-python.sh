#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Attempting to install Python..."
    
    # Install Python using the appropriate package manager based on the operating system
    if [[ "$(uname -s)" == "Linux" ]]; then
        apt-get update
        apt-get install -y python3
    else
        echo "Unsupported operating system. Please install Python manually."
        exit 1
    fi
    
    # Verify if Python installation was successful
    if ! command -v python3 &> /dev/null; then
        echo "Failed to install Python. Please install Python manually."
        exit 1
    fi
    
    echo "Python has been installed successfully."
fi

# chmod +x mapper.py reducer.py

echo "Python environment setup complete."

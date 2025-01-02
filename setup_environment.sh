#!/bin/bash

# Install ManimGL on macOS with nothing in place.

# Step 1: Install Homebrew (if not already installed)
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Step 2: Install Python (if not already installed)
if ! command -v python3 &> /dev/null; then
    echo "Installing Python..."
    brew install python
else
    echo "Python is already installed."
fi

# Step 3: Install FFmpeg (if not already installed)
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing FFmpeg..."
    brew install ffmpeg
else
    echo "FFmpeg is already installed."
fi

# Step 4: Install MacTeX (optional, for LaTeX support)
if ! command -v pdflatex &> /dev/null; then
    echo "Installing MacTeX..."
    brew install --cask mactex
else
    echo "MacTeX is already installed."
fi

# Step 5: Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv manimgl-env
source manimgl-env/bin/activate

# Step 6: Install ManimGL
echo "Installing ManimGL..."
pip install manimgl
pip install setuptools
pip install setuptools pydub


# Step 7: Verify the installation
echo "Verifying the installation..."
if ! command -v manimgl &> /dev/null; then
    echo "ManimGL installation failed. Please check the logs."
    exit 1
else
    echo "ManimGL installed successfully!"
fi

# Step 8: Run a test animation
echo "Running a test animation..."
cat << EOF > test.py
from manimlib import *

class TestAnimation(Scene):
    def construct(self):
        circle = Circle()
        self.play(ShowCreation(circle))

if __name__ == "__main__":
    TestAnimation().render()
EOF

manimgl test.py TestAnimation

# Step 9: Clean up
echo "Cleaning up..."
rm test.py

echo "Installation complete! To activate the virtual environment, run:"
echo "source manimgl-env/bin/activate"

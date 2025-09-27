#!/bin/bash

echo "Installing Waveshare e-ink display library locally..."

# Remove existing e-Paper directory if it exists
if [ -d "e-Paper" ]; then
    echo "Removing existing e-Paper directory..."
    rm -rf e-Paper
fi

# Clone the Waveshare e-Paper repository
echo "Cloning Waveshare repository..."
git clone https://github.com/waveshare/e-Paper.git

# Find the correct path for epd2in13_V4.py
echo "Looking for epd2in13_V4.py..."
find e-Paper -name "epd2in13_V4.py" -type f

# Copy files to current directory for local use
echo "Copying files to current directory..."
cp e-Paper/RaspberryPi_JetsonNano/python/lib/epd2in13_V4.py ./
cp -r e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd ./

# Install Python dependencies using apt
echo "Installing Python dependencies via apt..."
sudo apt update
sudo apt install -y python3-psutil python3-pil

echo "Installation complete!"
echo "Files copied locally. You can now run: python3 ink.py"

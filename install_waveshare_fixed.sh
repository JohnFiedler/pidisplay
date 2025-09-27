#!/bin/bash

echo "Installing Waveshare e-ink display library..."

# Remove existing e-Paper directory if it exists
if [ -d "e-Paper" ]; then
    echo "Removing existing e-Paper directory..."
    rm -rf e-Paper
fi

# Clone the Waveshare e-Paper repository
echo "Cloning Waveshare repository..."
git clone https://github.com/waveshare/e-Paper.git

# Check if the files exist
if [ ! -f "e-Paper/RaspberryPi_JetsonNano/python/lib/epd2in13_V4.py" ]; then
    echo "Error: epd2in13_V4.py not found. Checking directory structure..."
    find e-Paper -name "*.py" | grep -i epd
    exit 1
fi

# Create the target directory if it doesn't exist
sudo mkdir -p /usr/local/lib/python3/dist-packages/

# Copy the library files
echo "Copying library files..."
sudo cp -r e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd /usr/local/lib/python3/dist-packages/
sudo cp e-Paper/RaspberryPi_JetsonNano/python/lib/epd2in13_V4.py /usr/local/lib/python3/dist-packages/

# Install Python dependencies using apt (system packages)
echo "Installing Python dependencies via apt..."
sudo apt update
sudo apt install -y python3-psutil python3-pil

# Also try pip with --break-system-packages if needed
echo "Installing additional packages via pip..."
pip3 install --break-system-packages psutil pillow

# Clean up
rm -rf e-Paper

echo "Installation complete!"
echo "You can now run: python3 ink.py"

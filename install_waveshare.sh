#!/bin/bash

# Install Waveshare e-ink display library for 2.13 inch V4
echo "Installing Waveshare e-ink display library..."

# Clone the Waveshare e-ink repository
git clone https://github.com/waveshare/e-Paper.git

# Copy the Python library files
sudo cp -r e-Paper/RaspberryPi_JetsonNano/python/lib/waveshare_epd /usr/local/lib/python3/dist-packages/
sudo cp e-Paper/RaspberryPi_JetsonNano/python/lib/epd2in13_V4.py /usr/local/lib/python3/dist-packages/

# Install Python dependencies
pip3 install -r requirements.txt

# Clean up
rm -rf e-Paper

echo "Installation complete!"
echo "You can now run: python3 ink.py"

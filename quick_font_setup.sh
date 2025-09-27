#!/bin/bash

echo "Quick cyberpunk font setup for Pi Display..."

# Install required packages
sudo apt update
sudo apt install -y wget unzip fontconfig

# Create fonts directory
mkdir -p /home/pi/.fonts

# Download Orbitron font using curl (more reliable)
echo "Downloading Orbitron font..."
curl -L -o /home/pi/.fonts/Orbitron-Regular.ttf "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron-Regular.ttf"
curl -L -o /home/pi/.fonts/Orbitron-Bold.ttf "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron-Bold.ttf"

# Also try downloading from a different source
echo "Trying alternative download..."
wget -O /tmp/orbitron.zip "https://fonts.google.com/download?family=Orbitron"
if [ -f /tmp/orbitron.zip ]; then
    unzip -j /tmp/orbitron.zip "*.ttf" -d /home/pi/.fonts/
    echo "Downloaded from Google Fonts API"
fi

# Set permissions
chmod 644 /home/pi/.fonts/*.ttf

# List what we have
echo "Fonts in directory:"
ls -la /home/pi/.fonts/

# Update font cache
fc-cache -fv /home/pi/.fonts/

echo "Fonts installed! Restarting the display script..."
sudo systemctl restart pidisplay.service

echo "Done! Check the display for cyberpunk fonts."

#!/bin/bash

echo "Setting up cyberpunk fonts for Pi Display..."

# Create fonts directory
echo "Creating fonts directory..."
mkdir -p /home/pi/.fonts

# Download cyberpunk fonts
echo "Downloading cyberpunk fonts..."

# Download Orbitron (futuristic/cyberpunk font)
wget -O /tmp/orbitron.zip "https://fonts.google.com/download?family=Orbitron"
if [ -f /tmp/orbitron.zip ]; then
    unzip -j /tmp/orbitron.zip "*.ttf" -d /home/pi/.fonts/
    echo "Orbitron font installed"
fi

# Download Exo 2 (sci-fi font)
wget -O /tmp/exo2.zip "https://fonts.google.com/download?family=Exo%202"
if [ -f /tmp/exo2.zip ]; then
    unzip -j /tmp/exo2.zip "*.ttf" -d /home/pi/.fonts/
    echo "Exo 2 font installed"
fi

# Download Rajdhani (futuristic font)
wget -O /tmp/rajdhani.zip "https://fonts.google.com/download?family=Rajdhani"
if [ -f /tmp/rajdhani.zip ]; then
    unzip -j /tmp/rajdhani.zip "*.ttf" -d /home/pi/.fonts/
    echo "Rajdhani font installed"
fi

# Download Source Code Pro (monospace cyberpunk)
wget -O /tmp/sourcecodepro.zip "https://fonts.google.com/download?family=Source%20Code%20Pro"
if [ -f /tmp/sourcecodepro.zip ]; then
    unzip -j /tmp/sourcecodepro.zip "*.ttf" -d /home/pi/.fonts/
    echo "Source Code Pro font installed"
fi

# Update font cache
echo "Updating font cache..."
fc-cache -fv /home/pi/.fonts/

# Set permissions
chmod 644 /home/pi/.fonts/*.ttf

# List installed fonts
echo "Installed cyberpunk fonts:"
ls -la /home/pi/.fonts/

echo ""
echo "Cyberpunk fonts setup complete!"
echo "Available fonts:"
echo "  - Orbitron (futuristic)"
echo "  - Exo 2 (sci-fi)"
echo "  - Rajdhani (futuristic)"
echo "  - Source Code Pro (monospace)"
echo ""
echo "Fonts are now available for use in the Pi Display script."

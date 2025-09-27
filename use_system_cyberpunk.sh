#!/bin/bash

echo "Setting up cyberpunk fonts using system fonts..."

# Install additional system fonts that look more cyberpunk
sudo apt update
sudo apt install -y fonts-roboto fonts-roboto-mono fonts-liberation2

# Create a simple font directory
mkdir -p /home/pi/.fonts

# Copy some system fonts that look more futuristic
echo "Setting up system cyberpunk fonts..."

# Use Liberation Mono as a cyberpunk alternative (monospace)
cp /usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf /home/pi/.fonts/
cp /usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf /home/pi/.fonts/

# Use Roboto Mono as another option
cp /usr/share/fonts/truetype/roboto/unhinted/RobotoMono-Regular.ttf /home/pi/.fonts/
cp /usr/share/fonts/truetype/roboto/unhinted/RobotoMono-Bold.ttf /home/pi/.fonts/

# Set permissions
chmod 644 /home/pi/.fonts/*.ttf

# List what we have
echo "Fonts in directory:"
ls -la /home/pi/.fonts/

# Update font cache
fc-cache -fv /home/pi/.fonts/

echo "System cyberpunk fonts installed! Restarting the display script..."
sudo systemctl restart pidisplay.service

echo "Done! Check the display for monospace cyberpunk fonts."

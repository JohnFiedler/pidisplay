#!/bin/bash

echo "Setting up Pickle Rick custom faces for Pi Display..."

# Create custom-faces directory
echo "Creating /custom-faces directory..."
sudo mkdir -p /custom-faces

# Download the custom-faces from the repository
echo "Downloading Pickle Rick faces..."
cd /tmp

# Clone the repository (or download specific files)
if command -v git &> /dev/null; then
    echo "Cloning PWNAGOTCHI-CUSTOM-FACES-MOD repository..."
    git clone https://github.com/roodriiigooo/PWNAGOTCHI-CUSTOM-FACES-MOD.git
    if [ -d "PWNAGOTCHI-CUSTOM-FACES-MOD/custom-themes/pickle-rick/custom-faces" ]; then
        echo "Copying Pickle Rick faces..."
        sudo cp PWNAGOTCHI-CUSTOM-FACES-MOD/custom-themes/pickle-rick/custom-faces/*.png /custom-faces/
        echo "Pickle Rick faces copied to /custom-faces/"
    else
        echo "Pickle Rick theme not found in repository"
    fi
    # Clean up
    rm -rf PWNAGOTCHI-CUSTOM-FACES-MOD
else
    echo "Git not found. Please install git or manually download the faces."
    echo "You can download the faces from:"
    echo "https://github.com/roodriiigooo/PWNAGOTCHI-CUSTOM-FACES-MOD/tree/main/custom-themes/pickle-rick/custom-faces"
    echo "And place them in /custom-faces/"
fi

# Set permissions
echo "Setting permissions..."
sudo chmod 644 /custom-faces/*.png
sudo chown root:root /custom-faces/*.png

# List the files
echo "Files in /custom-faces/:"
ls -la /custom-faces/

echo "Setup complete! You can now run your ink.py script with Pickle Rick faces."

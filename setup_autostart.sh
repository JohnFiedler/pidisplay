#!/bin/bash

echo "Setting up Pi Display to start on boot..."

# Make sure we're in the right directory
cd /home/pi

# Copy the service file to systemd directory
echo "Installing systemd service..."
sudo cp pidisplay.service /etc/systemd/system/

# Reload systemd to recognize the new service
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "Enabling service to start on boot..."
sudo systemctl enable pidisplay.service

# Start the service now (optional)
echo "Starting service now..."
sudo systemctl start pidisplay.service

# Check status
echo "Checking service status..."
sudo systemctl status pidisplay.service

echo ""
echo "Setup complete!"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status pidisplay.service    # Check status"
echo "  sudo systemctl start pidisplay.service     # Start service"
echo "  sudo systemctl stop pidisplay.service      # Stop service"
echo "  sudo systemctl restart pidisplay.service   # Restart service"
echo "  sudo systemctl disable pidisplay.service   # Disable auto-start"
echo "  journalctl -u pidisplay.service -f         # View logs"
echo ""

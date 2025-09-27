#!/bin/bash

echo "Uploading files to Raspberry Pi..."

# Upload ink.py
echo "Uploading ink.py..."
scp ink.py pi@10.0.0.54:~/

# Upload setup script
echo "Uploading setup_rick_faces.sh..."
scp setup_rick_faces.sh pi@10.0.0.54:~/

echo "Upload complete!"

@echo off
echo Setting up cyberpunk fonts for Pi Display...

echo Uploading files to Raspberry Pi...
scp ink.py setup_cyberpunk_fonts.sh pi@10.0.0.54:~/

echo.
echo Connecting to Pi to install cyberpunk fonts...
ssh pi@10.0.0.54 "chmod +x setup_cyberpunk_fonts.sh && ./setup_cyberpunk_fonts.sh"

echo.
echo Cyberpunk fonts setup complete!
echo The Pi Display will now use futuristic cyberpunk fonts.
pause

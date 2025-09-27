@echo off
echo Setting up Pi Display autostart...

echo Uploading files to Raspberry Pi...
scp ink.py pidisplay.service setup_autostart.sh pi@10.0.0.54:~/

echo.
echo Connecting to Pi to run setup...
ssh pi@10.0.0.54 "chmod +x setup_autostart.sh && ./setup_autostart.sh"

echo.
echo Setup complete! The Pi Display will now start automatically on boot.
pause

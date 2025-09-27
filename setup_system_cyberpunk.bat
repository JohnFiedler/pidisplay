@echo off
echo Setting up system cyberpunk fonts for Pi Display...

echo Uploading files...
scp ink.py use_system_cyberpunk.sh pi@10.0.0.54:~/

echo.
echo Installing system cyberpunk fonts...
ssh pi@10.0.0.54 "chmod +x use_system_cyberpunk.sh && ./use_system_cyberpunk.sh"

echo.
echo System cyberpunk fonts setup complete!
echo The display should now use monospace fonts that look more cyberpunk.
pause

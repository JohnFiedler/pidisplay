@echo off
echo Installing cyberpunk fonts on Pi Display...

echo Uploading font setup script...
scp quick_font_setup.sh pi@10.0.0.54:~/

echo.
echo Running font installation on Pi...
ssh pi@10.0.0.54 "chmod +x quick_font_setup.sh && ./quick_font_setup.sh"

echo.
echo Cyberpunk fonts installation complete!
echo The display should now show futuristic fonts.
pause

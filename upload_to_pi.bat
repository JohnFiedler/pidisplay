@echo off
echo Uploading files to Raspberry Pi...

REM Upload ink.py
echo Uploading ink.py...
scp ink.py pi@10.0.0.54:~/

REM Upload setup script
echo Uploading setup_rick_faces.sh...
scp setup_rick_faces.sh pi@10.0.0.54:~/

echo Upload complete!
pause

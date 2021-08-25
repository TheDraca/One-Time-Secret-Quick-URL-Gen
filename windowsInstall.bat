@echo off

:: Check if we have python
python --version 3
if errorlevel 1 goto NoPython3

echo "Installing requests just in case it isn't already"
pip3 install requests
echo.
echo.
echo.

::Create folder if it doesn't exist
if not exist "%localappdata%\ots\" mkdir "%localappdata%\ots\"

::Move files
copy ots.pyw "%localappdata%\ots\" 
copy JsonControl.py "%localappdata%\ots\" 
copy ots.lnk "%AppData%\Microsoft\Windows\Start Menu\Programs"

if exist "%localappdata%\ots\OTS.json" echo "WARNING: You already have OTS.json file watch out if there have been any changes to the file "



echo "OTS should now been installed to %localappdata%\ots\"
echo "You may now delete these files, run OTS from your start menu now to setup your API Username/Password if needed"
pause
goto: eof


:NoPython3
echo "Python3 is not installed, please first download it here: https://www.python.org/downloads/"
pause

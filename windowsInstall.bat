@echo off
::Create folder if it doesn't exist
if not exist "%localappdata%\ots\" mkdir "%localappdata%\ots\"

::Move files
copy ots.pyw "%localappdata%\ots\" 
copy JsonControl.py "%localappdata%\ots\" 
copy OTS.json "%localappdata%\ots\" 
copy ots.lnk "%AppData%\Microsoft\Windows\Start Menu\Programs"



echo "OTS should now been installed to %localappdata%\ots\"
echo "You may now delete these files, run OTS from your start menu now to setup your API Username/Password"

pause

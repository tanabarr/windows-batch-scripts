@echo off
cd "C:\win scripts" 
start_first_VM.bat
mount_first_VM.bat
view_first_VM.bat

:: now we have mount loaded, pycharm should also load project chroma
::start "" "C:\Program Files (x86)\JetBrains\PyCharm 4.5.4\bin\pycharm.exe"
::choice /c yn /t 2 /d y >NUL		

exit

::@echo off
cd "C:\win scripts" 
start start_first_VM.bat
choice /c yn /t 6 /d y >NUL		
start mount_first_VM.bat
choice /c yn /t 6 /d y >NUL		
start view_first_VM.bat
start view_gateway_VM.bat

:: now we have mount loaded, pycharm should also load project chroma
::start "" "C:\Program Files (x86)\JetBrains\PyCharm 4.5.4\bin\pycharm.exe"


exit

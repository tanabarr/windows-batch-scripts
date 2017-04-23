@echo off
cd "C:\win scripts" 
start putty.exe -load "first VM"
start putty.exe -load "lotus-32vm2"

:: now we have mount loaded, pycharm should also load project chroma
::start "" "C:\Program Files (x86)\JetBrains\PyCharm 4.5.4\bin\pycharm.exe"
::choice /c yn /t 2 /d y >NUL		

exit

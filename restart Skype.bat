::Skype loses connection when we switch between networks (vpn/on-site)

cd "C:\Program Files (x86)\Skype\Phone"
SET Appname=Skype.exe
SET Uf="c:\Users\%USERNAME%\Desktop\tlSkype.txt"
SET Ud="c:\Users\%USERNAME%\Desktop\dbgSkype.log"
del /F %Ud%

:START
tasklist > %Uf%
find /C "%Appname%" %Uf%
IF ERRORLEVEL==1 GOTO END    
taskkill /F /IM %Appname% >> %Ud%
choice /c yn /t 8 /d y >NUL		
GOTO START
:END

:: Once shutdown, restart 
start /B %Appname%
choice /c yn /t 5 /d y >NUL		

:: Remove the temporary file 
del /F %Uf%

:FIN

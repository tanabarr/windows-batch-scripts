:: Initially try to shut down cleanly, then force. Restart Explorer to update
:: QuickStart items on taskbar on desktop
:: run from the desktop now
:: take a single commandline parameter for profile username

:: If this script is called with no commandline arguments specifying a profile
:: we want to use the previously set DNS_ARGS. If this is unset after reboot
:: Dragon will just load the previously used profile. So if script called
:: not through detection of a new device, we will load previous profile.
::SET DNS_ARGS=/user "Jabra BIZ"

IF NOT "%~1"=="" SET DNS_ARGS=/user "%~1"

::%DNS_ARGS%

cd "C:\Program Files (x86)\Nuance\NaturallySpeaking13\Program"
SET Uf="c:\Users\%USERNAME%\Desktop\tl1.txt"
SET Ud="c:\Users\%USERNAME%\Desktop\dbg.log"
del /F %Ud%

:START
tasklist > %Uf%
find /C "natspeak.exe" %Uf%
IF ERRORLEVEL==1 GOTO END    
taskkill /IM natspeak.exe /F >> %Ud%
choice /c yn /t 8 /d y >NUL		
GOTO START
:END

:: Once shutdown, restart 
start /B natspeak.exe %DNS_ARGS%
choice /c yn /t 5 /d y >NUL		

:: Remove the temporary file 
del /F %Uf%

:: Restart Explorer to update desktop context 
taskkill /F /IM explorer.exe 
choice /c yn /t 5 /d y >NUL		
cd "C:\Windows" 
start /B explorer.exe

:FIN
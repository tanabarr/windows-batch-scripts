REM =======================================================================================
REM =   INACTIVEPUTTYCHECK - Check for inactive putty windows
REM =======================================================================================
REM kill all running puttys (owned by system)
FOR /F "usebackq tokens=2 skip=2" %%p IN (`tasklist.exe /V /FO TABLE /NH /FI "IMAGENAME eq putty.exe"`) DO taskkill.exe /F /PID %%p /T >nul 2>&1
EXIT /B

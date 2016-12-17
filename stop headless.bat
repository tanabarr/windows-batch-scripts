:: wrapper script
runas /profile /user:GER\tanabarr "C:\win scripts\_stop_headless.bat"

choice /c yn /t 2 /d y >NUL		
exit
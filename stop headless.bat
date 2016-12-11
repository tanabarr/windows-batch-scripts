:: for some reason when using natlink/unimacro "file <this filename>" voice command,
:: PATH is not the same as on an interactive session (still broken)
C:\Windows\System32\umount.exe h:
C:\Windows\System32\umount.exe g:

:: saves VM
cd "c:\Program Files\Oracle\VirtualBox"
vboxmanage.exe controlvm "Centos67imldev" savestate
choice /c yn /t 2 /d y >NUL		

:: saves VM
cd "c:\Program Files\Oracle\VirtualBox"
vboxmanage.exe controlvm "Centos71imlnode" savestate
choice /c yn /t 2 /d y >NUL		

exit
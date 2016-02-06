:: saves VM
cd "c:\Program Files\Oracle\VirtualBox"
vboxmanage.exe controlvm "Centos67imldev" savestate
choice /c yn /t 8 /d y >NUL		

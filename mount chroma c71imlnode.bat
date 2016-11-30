:: starts VM then mounts share on VM
cd "c:\Program Files\Oracle\VirtualBox"
:: command implicitly waits for vm to load
vboxmanage.exe startvm "Centos71imlnode" --type headless
umount h:
choice /c yn /t 8 /d y >NUL		
mount -o fileaccess=644 \\192.168.56.102\export h:
choice /c yn /t 4 /d y >NUL		

:: open terminal to vm
start "" "C:\win scripts\second VM.bat"
choice /c yn /t 2 /d y >NUL		

exit


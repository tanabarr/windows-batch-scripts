:: starts VM then mounts share on VM
cd "c:\Program Files\Oracle\VirtualBox"
:: command implicitly waits for vm to load
vboxmanage.exe startvm "Centos67imldev" --type headless

umount g:
choice /c yn /t 6 /d y >NUL		
::mount -u:tanabarr -p:"..." \\192.168.56.102\home\share g:
mount -o fileaccess=644 \\192.168.56.101\home\share g:
choice /c yn /t 4 /d y >NUL		

@echo off
cd "C:\win scripts" 
start putty.exe -load "first VM"
start putty.exe -load "lotus-32vm2"

:: now we have mount loaded, pycharm should also load project chroma
::start "" "C:\Program Files (x86)\JetBrains\PyCharm 4.5.4\bin\pycharm.exe"
::choice /c yn /t 2 /d y >NUL		

exit

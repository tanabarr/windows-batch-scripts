:: starts VM then mounts share on VM
cd "c:\Program Files\Oracle\VirtualBox"
:: command implicitly waits for vm to load
vboxmanage.exe startvm "Centos7imldev" --type headless

:: currently don't need to mount as I am not using windows-based IDE on this VM (vim only)
:: therefore we also don't need to run in administrator mode from a wrapper
::umount h:
::choice /c yn /t 4 /d y >NUL		
::mount -o fileaccess=777 \\192.168.56.102\export h:
::choice /c yn /t 4 /d y >NUL		

@echo off
cd "C:\win scripts" 
start putty.exe -load "second VM"

exit
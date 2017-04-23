:: starts VM then mounts share on VM
::cd "c:\Program Files\Oracle\VirtualBox"
:: command implicitly waits for vm to load
::vboxmanage.exe startvm "Centos67imldev" --type headless
umount g:
choice /c yn /t 8 /d y >NUL		
::mount -u:tanabarr -p:"Chanch0306!" \\192.168.56.102\home\share g:
mount -o fileaccess=644 \\192.168.56.101\home\share g:
choice /c yn /t 4 /d y >NUL		

:: now we have mount loaded, pycharm should also load project chroma
::start "" "C:\Program Files (x86)\JetBrains\PyCharm 4.5.4\bin\pycharm.exe"
::choice /c yn /t 2 /d y >NUL		

:: open terminal to vm
::start "" "C:\win scripts\first VM.bat"
::choice /c yn /t 2 /d y >NUL		

exit

::unrelated and should really be somewhere else! change UAC
::c:\Windows\System32\UserAccountControlSettings.exe



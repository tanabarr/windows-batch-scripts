:: starts VM
cd "c:\Program Files\Oracle\VirtualBox"
:: command implicitly waits for vm to load
vboxmanage.exe startvm "Centos71imlnode" --type headless
choice /c yn /t 8 /d y >NUL		

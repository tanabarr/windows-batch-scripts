cd c:\Android
::adb forward tcp:22 tcp:22
::adb forward tcp:5901 tcp:5901
::adb root 
adb shell "chmod 777 /data/davik-cache " 
adb shell "chmod 777 /data/davik-cache/* "
:: start remote viewer 1 (keyboard works)
:: for permissions to this batch file. Sound for nc? Keyboard shortcuts?
pause
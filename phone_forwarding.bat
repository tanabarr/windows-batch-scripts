:: Parent script for running android screencast and VNC
cd "c:\Program Files (x86)\Android\android-sdk-windows\platform-tools"
:adb backup -apk -shared -all
::adb shell "su" 
:adb root 
:adb shell "chmod 755 /data/dalvik-cache " 
:adb shell "cd /data/dalvik-cache"
:adb shell "chmod 755 ./* " 


:: Forward ports from vnc server on phone
:::adb forward tcp:22 tcp:22
::adb forward tcp:5958 tcp:5904
adb forward tcp:5905 tcp:5905
::adb forward tcp:5805 tcp:5804

:: start remote viewer 1 (keyboard works)
:cd c:\AndroidScreenCast
:androidscreencast.jnlp & 
:: Todo: don't seem to work together, driver web client instead is?
echo "Screencast keys: End Key = Power button Delete Key = Back button"
echo "Home key = Home button Pg Up Key = Menu button Pg Dn Key = Dialer button"
 
:pause
:: start remote viewer 2 (mouse works)
cd "C:\Program Files (x86)\TightVNC"
vncviewer.exe localhost:5905
::vncviewer.exe localhost:5958
:: Note: does not like running as background process?? Cannot be 
:: will not run after screen cast, which has to be started afterwards
pause

::NOTE: the significant

:: start of ssh connection with the phone 
::cd "C:\Program Files\PuTTY"
::start putty.exe -load "android_phone" &
::TODO: works great, ctrl+left to move one window to one side and
:: same as other window to move to the right.
:: "close window" voice recognition command somehow rotates
:: tightvnc screen. Repeat until upright. (natlink script required)
:: add dalvik-cache fixed for android screen cast (from website)
:: for permissions to this batch file. Sound for nc? Keyboard shortcuts?
:10.228.34.38:5901
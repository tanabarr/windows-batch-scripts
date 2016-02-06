:: Backup android phone (all), creates backup.ab in working directory (platform-tools below)
cd "c:\Program Files (x86)\Android\android-sdk-windows\platform-tools"
adb backup -apk -shared -all

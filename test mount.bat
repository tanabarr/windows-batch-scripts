:: http://stackoverflow.com/questions/11525056/how-to-create-a-batch-file-to-run-cmd-as-administrator
cd "C:\win scripts"
runas /user:GER\tanabarr _mount.bat
::runas /user:GER\tanabarr _mount.bat < tmp.txt
::type tmp.txt | runas /user:GER\tanabarr _mount.bat
::runas /noprofile /user:GER\tanabarr "C:\win scripts\_mount.bat"

choice /c yn /t 8 /d y >NUL		
exit
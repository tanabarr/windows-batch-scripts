:: batch wrapper to open text files in Windows with vim 
:: commands and commandline parameters executed by the vim instance within cygwin terminal
echo off
::echo %*
::pause
start "gvim" "c:/Program Files (x86)/Vim/vim74/gvim.exe" --remote-tab-silent %1
::start "gvim" "c:/Program Files (x86)/Vim/vim74/gvim.exe --remote-tab-silent %*"
::chdir C:\Users\tan.000\Dropbox\cygwin\bin
::start mintty.exe /bin/vim.exe -u ~/.vimrc %1

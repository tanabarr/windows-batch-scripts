:: Batch script to update ownership and permission inheritance
:: of off-line files to become accessible by local Administrator
:: Needs to be executed between when off-line file modification/sync
:: and when backed up on stand-alone system. Otherwise modified files
:: will not have correct ownerships and inherited permissions.
:: Add key to HKEY_LM/SOFTWARE/Microsoft/Windows/currentversion/Run:
:: "C:\Uses\tan.000\Documents\win scripts\off-line_perm_update.bat"
:: seems to not like wild card expansion in the middle of pathname
:: icacls.

takeown /F C:\Windows\CSC\v2.0.6\namespace\us-o* /R /A /D Y

icacls C:\Windows\CSC\v2.0.6\namespace\us-oakland\* /inheritance:e /T /C

pause
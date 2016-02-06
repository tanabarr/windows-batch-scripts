@echo off
cd "c:/win scripts/iphone"
:: begin usb tunnel for ssh (winscp) & vnc
START /B CMD /C CALL itunnel_mux --lport 2223 --iport 22
START /B CMD /C CALL itunnel_mux --lport 5904 --iport 5900
::"Mobile screen.vnc"

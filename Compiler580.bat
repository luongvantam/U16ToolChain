@echo off
:main
cls
cd /d "%~dp0"
set /p name="Enter your filename to compile (for 580VNX only): "
cls 
python compiler/580vnx/compiler_.py -f hex < rsc_ropchain/%name%.rsc
echo.
echo Press any key to compile next file or compile again...
pause>nul
goto main
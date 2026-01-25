@echo off
rem
if not exist "hex_ropchain" mkdir "hex_ropchain"
if not exist "asm_ropchain" mkdir "asm_ropchain"

:loop
cls
set "filename="
set /p "filename=Enter your filename to decompile (only fx580vnx): "

set "hex_file_path=..\hex_ropchain\%filename%.txt"
set "asm_file_path=..\asm_ropchain\%filename%.asm"

if not exist "%hex_file_path%" (
    echo Error: File '%hex_file_path%' not found!
    echo Press any key to try again...
    pause > nul
    goto :loop
)

echo Decompiling '%filename%.txt'...
python main.py "580vnx" "%hex_file_path%" "%asm_file_path%"

if %errorlevel% equ 0 (
    echo.
    echo Decompilation complete. Output saved to '%asm_file_path%'
) else (
    echo An error occurred while running the decompiler script.
)

timeout /t 1 /nobreak > nul
echo Press any key to continue...
pause > nul
goto :loop
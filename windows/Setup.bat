@echo off
rem  Yangi ozbek klaviatura layoutlari - ornatish/ochirish oynasini ochadi.
rem  Ikki marta bosing. Administrator huquqi (UAC) sorashi mumkin.
rem  Buyruq satri: Setup.bat -Action Install -Layout uzq,uzcw
rem               Setup.bat -Action Uninstall -Layout uzq,uzcw
setlocal
cd /d "%~dp0"
if not exist "%~dp0Setup.ps1" (
    echo Setup.ps1 topilmadi. ZIP arxivni to'liq chiqaring ^(Extract All^).
    pause
    exit /b 1
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Setup.ps1" %*
if errorlevel 1 pause

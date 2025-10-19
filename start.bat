@echo off
echo ==================================
echo   ATAK Kulubu Baslat
echo ==================================
echo.

REM Virtual environment kontrol
if not exist "venv" (
    echo [!] Virtual environment bulunamadi!
    echo [*] Lutfen once setup.ps1 scriptini calistirin.
    pause
    exit /b
)

echo [+] Virtual environment aktif ediliyor...
call venv\Scripts\activate.bat

echo.
echo [+] Uygulama baslatiliyor...
echo [*] Durdurmak icin CTRL+C yapin
echo.
echo Uygulama http://127.0.0.1:5000 adresinde calisacaktir.
echo.

python run.py

pause

@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv || exit /b 1
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements-build.txt || exit /b 1
pyinstaller --clean -y RedirectVPNspoof.spec || exit /b 1
echo.
echo ======================================================
echo Done. Executable: dist\RedirectVPNspoof.exe
echo ======================================================

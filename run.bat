@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo [setup] Creating virtual environment .venv ...
    python -m venv .venv || goto :err
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt || goto :err
) else (
    call .venv\Scripts\activate.bat
)
python run.py %*
goto :eof
:err
echo [error] setup failed
exit /b 1

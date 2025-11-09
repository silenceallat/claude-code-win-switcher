@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Multi-AI Environment Manager
echo ========================================
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Current directory: %CD%
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python not found
    echo Please install Python 3.7+ and add to PATH
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python: %PYTHON_VERSION%
echo.

REM Install Flask if needed
python -c "import flask" >nul 2>&1
if %errorLevel% neq 0 (
    echo Installing Flask...
    python -m pip install flask==2.3.3
    if %errorLevel% neq 0 (
        echo ERROR: Flask installation failed
        pause
        exit /b 1
    )
    echo Flask installed successfully
) else (
    echo Flask: already installed
)
echo.

REM Start the application without UAC prompt
echo Starting application...
echo ========================================
echo   Server: http://localhost:5000
echo   Press Ctrl+C to stop
echo ========================================
echo.

python app.py

pause
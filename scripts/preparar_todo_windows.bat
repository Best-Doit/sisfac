@echo off
REM Script TODO-EN-UNO para Windows
REM - Instala Python (verifica)
REM - Instala Node.js y Electron (si no están)
REM - Prepara entorno completo

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ================================
echo   Preparar TODO SISFAC (Windows)
echo   Python + Node.js + Electron
echo ================================
echo.

SET ROOT_DIR=%~dp0..
PUSHD "%ROOT_DIR%"

REM Paso 1: Python
echo [1/3] Preparando Python...
CALL "%~dp0preparar_entorno_windows.bat"
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la preparacion de Python.
    EXIT /B 1
)

REM Paso 2: Node.js y Electron
echo.
echo [2/3] Preparando Node.js y Electron...
CALL "%~dp0instalar_nodejs_electron_windows.bat"
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la instalacion de Node.js/Electron.
    EXIT /B 1
)

REM Paso 3: Verificación final
echo.
echo [3/3] Verificacion final...
echo.
echo Python:
python --version
echo.
echo Node.js:
node --version
echo.
echo Electron:
CD electron
npm list electron --depth=0
CD ..

echo.
echo ================================
echo   TODO LISTO!
echo ================================
echo.
echo Puedes:
echo   1. Iniciar la aplicacion:
echo      venv\Scripts\activate
echo      cd backend
echo      python run.py
echo.
echo   2. Empaquetar la aplicacion:
echo      scripts\empaquetar_windows.bat
echo.

POPD
ENDLOCAL


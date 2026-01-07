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
echo [1/3] Preparando Python y dependencias...
echo   Instalando Python y todas las dependencias del proyecto...
CALL "%~dp0preparar_entorno_windows.bat"
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la preparacion de Python.
    EXIT /B 1
)
echo   Python y dependencias instaladas correctamente.

REM Paso 2: Node.js y Electron
echo.
echo [2/3] Preparando Node.js y Electron...
echo   Instalando Node.js (si no esta) y Electron en el proyecto...
CALL "%~dp0instalar_nodejs_electron_windows.bat"
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la instalacion de Node.js/Electron.
    EXIT /B 1
)
echo   Node.js y Electron instalados correctamente.

REM Paso 3: Verificación final
echo.
echo [3/3] Verificacion final...
echo.

REM Verificar Python en venv
echo Verificando Python en entorno virtual...
CALL venv\Scripts\activate.bat
python --version
python -c "import flask; print('Flask:', flask.__version__)" 2>NUL
python -c "import PyInstaller; print('PyInstaller: OK')" 2>NUL
deactivate 2>NUL

echo.
echo Verificando Node.js:
node --version 2>NUL || echo   Node.js no encontrado en PATH

echo.
echo Verificando Electron:
CD electron
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo cambiar al directorio electron
    EXIT /B 1
)
npm list electron --depth=0 2>NUL || echo   Electron no encontrado
npm list electron-builder --depth=0 2>NUL || echo   electron-builder no encontrado
CD ..
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo volver al directorio raiz
    EXIT /B 1
)

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


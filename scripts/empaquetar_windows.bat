@echo off
REM Script para empaquetar SISFAC completo en Windows
REM Incluye: Backend (PyInstaller) + Frontend (Electron, instalador NSIS)

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ================================
echo   Empaquetar SISFAC - Windows
echo ================================
echo.

REM Detectar ruta del proyecto (directorio de este script)
SET SCRIPT_DIR=%~dp0
PUSHD "%SCRIPT_DIR%\.."

REM Paso 1: Backend con PyInstaller
echo [1/2] Compilando backend con PyInstaller...

SET VENV_DIR=%CD%\venv
IF EXIST "%VENV_DIR%\Scripts\activate.bat" (
    echo   Activando entorno virtual...
    CALL "%VENV_DIR%\Scripts\activate.bat"
    SET PYTHON_CMD=python
    SET PIP_CMD=pip
) ELSE (
    echo   No se encontro venv, usando Python del sistema...
    SET PYTHON_CMD=python
    SET PIP_CMD=pip
)

CD backend

REM Verificar PyInstaller
%PYTHON_CMD% -c "import PyInstaller" 2>NUL
IF ERRORLEVEL 1 (
    echo   PyInstaller no esta instalado. Instalando...
    %PIP_CMD% install pyinstaller
)

echo   Limpiando compilaciones anteriores...
IF EXIST build RMDIR /S /Q build
IF EXIST dist RMDIR /S /Q dist

echo   Compilando backend (sisfac-backend.spec)...
%PYTHON_CMD% -m PyInstaller sisfac-backend.spec
IF NOT EXIST "dist\sisfac-backend.exe" (
    echo.
    echo   ERROR: No se genero dist\sisfac-backend.exe
    EXIT /B 1
)

echo   Backend compilado correctamente: backend\dist\sisfac-backend.exe

CD ..

REM Paso 2: Empaquetar Electron para Windows
echo.
echo [2/2] Empaquetando aplicacion Electron (instalador Windows)...

CD electron

REM Verificar dependencias de Electron
IF NOT EXIST "node_modules" (
    echo   Instalando dependencias de Electron...
    npm install
)

echo   Ejecutando electron-builder para Windows...
npm run build:win
IF ERRORLEVEL 1 (
    echo.
    echo   ERROR: Fallo electron-builder (npm run build:win)
    EXIT /B 1
)

echo.
echo Empaquetado completado.
echo Revisa la carpeta: %CD%\dist
echo (Deberias ver el instalador, por ejemplo: "SISFAC Setup 1.0.0.exe")

POPD
ENDLOCAL


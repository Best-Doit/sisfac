@echo off
REM Script para empaquetar SISFAC como instalador .exe para Windows
REM Objetivo: Aplicación autónoma sin dependencias externas

setlocal enabledelayedexpansion

echo.
echo 🚀 Empaquetando SISFAC como instalador .exe para Windows...
echo.

REM Directorios
set "ROOT_DIR=%~dp0"
set "VENV_PATH=%ROOT_DIR%venv"
set "BACKEND_DIR=%ROOT_DIR%backend"
set "ELECTRON_DIR=%ROOT_DIR%electron"

REM Paso 1: Compilar backend con PyInstaller
echo 📦 Paso 1: Compilando backend...
cd /d "%BACKEND_DIR%"

REM Verificar entorno virtual
if not exist "%VENV_PATH%" (
    echo ❌ Error: Entorno virtual no encontrado en %VENV_PATH%
    echo    Por favor, ejecuta start.bat primero para crear el entorno virtual.
    pause
    exit /b 1
)

REM Resolver Python del entorno virtual
set "VENV_PYTHON=%VENV_PATH%\Scripts\python.exe"
if not exist "%VENV_PYTHON%" (
    echo ❌ Error: Python del venv no encontrado en %VENV_PYTHON%
    echo    Por favor, ejecuta start.bat primero para crear el entorno virtual.
    pause
    exit /b 1
)

REM Verificar dependencias del backend
"%VENV_PYTHON%" -c "import flask" 2>nul
if errorlevel 1 (
    echo 📦 Instalando dependencias del backend...
    "%VENV_PYTHON%" -m pip install -r "%ROOT_DIR%requirements.txt"
    if errorlevel 1 (
        echo ❌ Error: Falló la instalación de dependencias del backend
        pause
        exit /b 1
    )
)

REM Verificar PyInstaller
"%VENV_PYTHON%" -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 📦 Instalando PyInstaller...
    "%VENV_PYTHON%" -m pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Error: No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
)

REM Limpiar compilaciones anteriores
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Compilar con PyInstaller
echo 📦 Compilando backend con PyInstaller...
"%VENV_PYTHON%" -m PyInstaller sisfac-backend.spec --clean --noconfirm

if not exist "dist\sisfac-backend.exe" (
    echo ❌ Error: Backend no compilado correctamente
    echo    Se esperaba: dist\sisfac-backend.exe
    pause
    exit /b 1
)

echo ✅ Backend compilado: dist\sisfac-backend.exe
cd /d "%ROOT_DIR%"

REM Paso 2: Empaquetar con Electron
echo.
echo 📦 Paso 2: Empaquetando con Electron...
cd /d "%ELECTRON_DIR%"

REM Verificar Node.js
where node >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Node.js no encontrado
    echo    Por favor, instala Node.js desde https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar dependencias de Electron
if not exist "node_modules" (
    echo 📦 Instalando dependencias de Electron...
    call npm install
    if errorlevel 1 (
        echo ❌ Error: Falló la instalación de dependencias de Electron
        pause
        exit /b 1
    )
) else (
    if not exist "node_modules\electron-builder" (
        echo 📦 Instalando dependencias de Electron...
        call npm install
        if errorlevel 1 (
            echo ❌ Error: Falló la instalación de dependencias de Electron
            pause
            exit /b 1
        )
    )
)

REM Verificar recursos de Windows (icono + NSIS include)
if not exist "build\installer.nsh" (
    echo 🧩 Creando build\installer.nsh...
    >"build\installer.nsh" (
        echo ; NSIS include file for SISFAC installer
        echo ; Reserved for future customizations.
    )
)

if not exist "build\icon.ico" (
    if not exist "build\icon.png" (
        echo ❌ Error: No se encontró build\icon.png para generar icon.ico
        pause
        exit /b 1
    )
    echo 🎨 Generando build\icon.ico desde icon.png...
    npx -y png-to-ico build\icon.png > build\icon.ico
    if errorlevel 1 (
        echo ❌ Error: No se pudo generar build\icon.ico (requiere npx/npm)
        pause
        exit /b 1
    )
)

REM Limpiar builds anteriores
if exist "dist" rmdir /s /q dist

REM Empaquetar para Windows
echo 📦 Generando instalador .exe...
call npm run dist:win
if errorlevel 1 (
    echo ❌ Error: Falló el empaquetado con Electron
    pause
    exit /b 1
)

REM Buscar archivo .exe generado
set "INSTALLER="
for /r dist %%f in (*.exe) do (
    echo %%f | findstr /i "\\win-unpacked\\" >nul
    if errorlevel 1 if "%%~nxf" neq "sisfac-backend.exe" (
        set "INSTALLER=%%f"
        goto :found
    )
)
:found

echo.
if defined INSTALLER (
    for %%A in ("%INSTALLER%") do set "SIZE=%%~zA"
    set /a SIZE_MB=!SIZE! / 1048576
    echo ✅ ¡Empaquetado completado!
    echo.
    echo 📦 Instalador de Windows:
    echo    Archivo: %INSTALLER%
    echo    Tamaño: !SIZE_MB! MB
    echo.
    echo 📥 Para instalar, ejecuta el archivo .exe generado
    echo 💡 Después de instalar, busca 'SISFAC' en el menú de inicio
    echo 💡 Aplicación autónoma - NO requiere dependencias externas
) else (
    echo ❌ Error: No se generó el instalador .exe
    echo    Revisa los logs anteriores para más detalles
    pause
    exit /b 1
)

echo.
pause

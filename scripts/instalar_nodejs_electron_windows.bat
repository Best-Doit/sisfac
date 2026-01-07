@echo off
REM Script automatizado para instalar Node.js y Electron en Windows
REM - Verifica/instala Node.js
REM - Instala Electron y dependencias

SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ================================
echo   Instalar Node.js y Electron
echo   (Windows - Automatizado)
echo ================================
echo.

SET ROOT_DIR=%~dp0..
PUSHD "%ROOT_DIR%"

REM Paso 1: Verificar Node.js
echo [1/3] Verificando Node.js...
node --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo   Node.js no encontrado. Intentando instalar...
    echo.
    
    REM Intentar con Chocolatey
    where choco >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        echo   Instalando Node.js con Chocolatey...
        choco install nodejs-lts -y
        IF ERRORLEVEL 1 (
            echo   ERROR: Fallo la instalacion con Chocolatey.
            echo.
            echo   Por favor, instala Node.js manualmente:
            echo   1. Visita: https://nodejs.org/
            echo   2. Descarga la version LTS
            echo   3. Ejecuta el instalador
            echo   4. Reinicia la terminal
            echo   5. Ejecuta este script nuevamente
            EXIT /B 1
        )
        echo   Node.js instalado correctamente.
        echo   Por favor, CIERRA y ABRE una nueva terminal, luego ejecuta este script nuevamente.
        EXIT /B 0
    ) ELSE (
        echo   Chocolatey no encontrado.
        echo.
        echo   Por favor, instala Node.js manualmente:
        echo   1. Visita: https://nodejs.org/
        echo   2. Descarga la version LTS (recomendado)
        echo   3. Ejecuta el instalador .msi
        echo   4. Acepta todas las opciones por defecto
        echo   5. Reinicia la terminal
        echo   6. Ejecuta este script nuevamente
        echo.
        echo   O instala Chocolatey primero:
        echo   https://chocolatey.org/install
        EXIT /B 1
    )
) ELSE (
    echo   Node.js encontrado:
    node --version
    npm --version
    echo   Nota: Se recomienda Node.js 18 o superior para Electron 28.0.0
)

REM Paso 2: Verificar npm
echo.
echo [2/3] Verificando npm...
npm --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo   ERROR: npm no encontrado. Reinstala Node.js.
    EXIT /B 1
)
echo   npm encontrado:
npm --version

REM Paso 3: Instalar Electron
echo.
echo [3/3] Instalando Electron y dependencias...
CD electron
IF ERRORLEVEL 1 (
    echo   ERROR: No se pudo cambiar al directorio electron
    EXIT /B 1
)

echo   Limpiando instalacion anterior (si existe)...
IF EXIST "node_modules" (
    RMDIR /S /Q node_modules
)
IF EXIST "package-lock.json" (
    DEL /F /Q package-lock.json
)

echo   Instalando dependencias de Electron (esto puede tardar unos minutos)...
npm install
IF ERRORLEVEL 1 (
    echo   ERROR: Fallo la instalacion de Electron.
    echo   Intenta manualmente: cd electron ^&^& npm install
    EXIT /B 1
)

REM Verificar instalacion
echo.
echo Verificando instalacion...
npm list electron
npm list electron-builder

IF ERRORLEVEL 1 (
    echo   ERROR: Electron no se instalo correctamente.
    EXIT /B 1
)

echo.
echo ================================
echo   Instalacion completada!
echo ================================
echo.
echo Node.js: 
node --version
echo npm:
npm --version
echo Electron:
npm list electron --depth=0
echo electron-builder:
npm list electron-builder --depth=0
echo.
echo Puedes empaquetar la aplicacion con:
echo   scripts\empaquetar_windows.bat
echo.

POPD
ENDLOCAL


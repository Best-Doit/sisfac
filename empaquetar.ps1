# Script para empaquetar SISFAC como instalador .exe para Windows
# Objetivo: Aplicación autónoma sin dependencias externas

Write-Host ""
Write-Host "🚀 Empaquetando SISFAC como instalador .exe para Windows..." -ForegroundColor Cyan
Write-Host ""

# Directorios
$ROOT_DIR = $PSScriptRoot
$VENV_PATH = Join-Path $ROOT_DIR "venv"
$BACKEND_DIR = Join-Path $ROOT_DIR "backend"
$ELECTRON_DIR = Join-Path $ROOT_DIR "electron"

# Paso 1: Compilar backend con PyInstaller
Write-Host "📦 Paso 1: Compilando backend..." -ForegroundColor Yellow
Set-Location $BACKEND_DIR

# Verificar entorno virtual
if (-not (Test-Path $VENV_PATH)) {
    Write-Host "❌ Error: Entorno virtual no encontrado en $VENV_PATH" -ForegroundColor Red
    Write-Host "   Por favor, ejecuta start.ps1 primero para crear el entorno virtual." -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Resolver Python del entorno virtual
$venvPython = Join-Path $VENV_PATH "Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "❌ Error: Python del venv no encontrado en $venvPython" -ForegroundColor Red
    Write-Host "   Por favor, ejecuta start.ps1 primero para crear el entorno virtual." -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar dependencias del backend
$flaskInstalled = & $venvPython -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Instalando dependencias del backend..." -ForegroundColor Yellow
    & $venvPython -m pip install -r "$ROOT_DIR\requirements.txt"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: Falló la instalación de dependencias del backend" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Verificar PyInstaller
$pyInstallerInstalled = & $venvPython -c "import PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Instalando PyInstaller..." -ForegroundColor Yellow
    & $venvPython -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: No se pudo instalar PyInstaller" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Limpiar compilaciones anteriores
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

# Compilar con PyInstaller
Write-Host "📦 Compilando backend con PyInstaller..." -ForegroundColor Yellow
& $venvPython -m PyInstaller sisfac-backend.spec --clean --noconfirm

if (-not (Test-Path "dist\sisfac-backend.exe")) {
    Write-Host "❌ Error: Backend no compilado correctamente" -ForegroundColor Red
    Write-Host "   Se esperaba: dist\sisfac-backend.exe" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✅ Backend compilado: dist\sisfac-backend.exe" -ForegroundColor Green
Set-Location $ROOT_DIR

# Paso 2: Empaquetar con Electron
Write-Host ""
Write-Host "📦 Paso 2: Empaquetando con Electron..." -ForegroundColor Yellow
Set-Location $ELECTRON_DIR

# Verificar Node.js
$nodeExists = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeExists) {
    Write-Host "❌ Error: Node.js no encontrado" -ForegroundColor Red
    Write-Host "   Por favor, instala Node.js desde https://nodejs.org/" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Verificar dependencias de Electron
$electronBuilderPath = Join-Path $ELECTRON_DIR "node_modules\electron-builder"
if (-not (Test-Path "node_modules") -or -not (Test-Path $electronBuilderPath)) {
    Write-Host "📦 Instalando dependencias de Electron..." -ForegroundColor Yellow
    cmd /c "npm install"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: Falló la instalación de dependencias de Electron" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Verificar recursos de Windows (icono + NSIS include)
$iconIco = Join-Path $ELECTRON_DIR "build\icon.ico"
$iconPng = Join-Path $ELECTRON_DIR "build\icon.png"
$installerNsh = Join-Path $ELECTRON_DIR "build\installer.nsh"

if (-not (Test-Path $installerNsh)) {
    Write-Host "🧩 Creando build\\installer.nsh..." -ForegroundColor Yellow
    $installerNshContent = @'
; NSIS include file for SISFAC installer
; Reserved for future customizations.
'@
    Set-Content -NoNewline -Path $installerNsh -Value $installerNshContent
}

if (-not (Test-Path $iconIco)) {
    if (-not (Test-Path $iconPng)) {
        Write-Host "❌ Error: No se encontró build\\icon.png para generar icon.ico" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    Write-Host "🎨 Generando build\\icon.ico desde icon.png..." -ForegroundColor Yellow
    cmd /c "npx -y png-to-ico build\\icon.png > build\\icon.ico"
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $iconIco)) {
        Write-Host "❌ Error: No se pudo generar build\\icon.ico (requiere npx/npm)" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Limpiar builds anteriores
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

# Empaquetar para Windows
Write-Host "📦 Generando instalador .exe..." -ForegroundColor Yellow
cmd /c "npm run dist:win"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error: Falló el empaquetado con Electron" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Buscar archivo .exe generado
$installer = Get-ChildItem -Path "dist" -Filter "*.exe" -Recurse |
    Where-Object { $_.FullName -notmatch '\\win-unpacked\\' } |
    Where-Object { $_.Name -ne "sisfac-backend.exe" } | 
    Select-Object -First 1

Write-Host ""
if ($installer) {
    $sizeMB = [math]::Round($installer.Length / 1MB, 2)
    Write-Host "✅ ¡Empaquetado completado!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Instalador de Windows:" -ForegroundColor Cyan
    Write-Host "   Archivo: $($installer.FullName)" -ForegroundColor White
    Write-Host "   Tamaño: $sizeMB MB" -ForegroundColor White
    Write-Host ""
    Write-Host "📥 Para instalar, ejecuta el archivo .exe generado" -ForegroundColor Yellow
    Write-Host "💡 Después de instalar, busca 'SISFAC' en el menú de inicio" -ForegroundColor Yellow
    Write-Host "💡 Aplicación autónoma - NO requiere dependencias externas" -ForegroundColor Green
} else {
    Write-Host "❌ Error: No se generó el instalador .exe" -ForegroundColor Red
    Write-Host "   Revisa los logs anteriores para más detalles" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Read-Host "Presiona Enter para salir"

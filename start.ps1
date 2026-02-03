# Script de inicio para SISFAC en Windows (PowerShell)

Write-Host ""
Write-Host "🚀 Iniciando SISFAC..." -ForegroundColor Cyan
Write-Host ""

# Verificar si existe el entorno virtual
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: No se pudo crear el entorno virtual" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Activar entorno virtual
Write-Host "🔌 Activando entorno virtual..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Actualizar pip
Write-Host "📦 Actualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Verificar si las dependencias están instaladas
$flaskInstalled = python -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error: Falló la instalación de dependencias" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
}

# Cambiar al directorio backend
Set-Location backend

# Iniciar la aplicación
Write-Host ""
Write-Host "✅ Iniciando servidor Flask..." -ForegroundColor Green
Write-Host "🌐 Abre tu navegador en: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📝 Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""
python run.py

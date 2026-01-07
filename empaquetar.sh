#!/bin/bash
# Script para empaquetar SISFAC completo
# Incluye: Backend (PyInstaller) + Frontend (Electron)

set -e

echo "🚀 Iniciando empaquetado de SISFAC..."
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Recompilar backend con PyInstaller
echo -e "${YELLOW}📦 Paso 1: Recompilando backend con PyInstaller...${NC}"

# Detectar y activar entorno virtual
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$SCRIPT_DIR/venv"

if [ -d "$VENV_PATH" ]; then
    echo "🔧 Activando entorno virtual..."
    source "$VENV_PATH/bin/activate"
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "⚠️  No se encontró venv, usando Python del sistema..."
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

cd backend

# Verificar si PyInstaller está instalado
if ! $PYTHON_CMD -c "import PyInstaller" 2>/dev/null; then
    echo "⚠️  PyInstaller no está instalado. Instalando en el entorno virtual..."
    $PIP_CMD install pyinstaller
fi

# Limpiar compilaciones anteriores
echo "🧹 Limpiando compilaciones anteriores..."
rm -rf build/ dist/

# Compilar con PyInstaller usando el archivo .spec
echo "🔨 Compilando backend..."
$PYTHON_CMD -m PyInstaller sisfac-backend.spec

if [ -f "dist/sisfac-backend" ]; then
    echo -e "${GREEN}✅ Backend compilado correctamente${NC}"
    chmod +x dist/sisfac-backend
else
    echo "❌ Error: No se generó el ejecutable del backend"
    exit 1
fi

cd ..

# Desactivar venv si estaba activado
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate 2>/dev/null || true
fi

# Paso 2: Empaquetar con Electron
echo ""
echo -e "${YELLOW}📦 Paso 2: Empaquetando con Electron...${NC}"
cd electron

# Verificar si electron-builder está instalado
if ! npm list electron-builder >/dev/null 2>&1; then
    echo "⚠️  electron-builder no está instalado. Instalando..."
    npm install
fi

# Empaquetar AppImage
echo "🔨 Generando AppImage..."
npm run dist

if [ -f "dist/SISFAC-1.0.0.AppImage" ]; then
    echo ""
    echo -e "${GREEN}✅ ¡Empaquetado completado exitosamente!${NC}"
    echo ""
    echo "📦 Archivo generado:"
    echo "   $(pwd)/dist/SISFAC-1.0.0.AppImage"
    echo ""
    echo "🚀 Para ejecutar:"
    echo "   chmod +x dist/SISFAC-1.0.0.AppImage"
    echo "   ./dist/SISFAC-1.0.0.AppImage"
    echo ""
    echo "💡 O usa el script ejecutar_appimage.sh:"
    echo "   ./ejecutar_appimage.sh dist/SISFAC-1.0.0.AppImage"
else
    echo "❌ Error: No se generó el AppImage"
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}✨ Proceso completado${NC}"


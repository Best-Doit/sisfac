#!/bin/bash
# Script para empaquetar SISFAC como paquete DEB instalable
# Objetivo: Aplicación autónoma sin dependencias externas para Kubuntu/Ubuntu

set -e

echo "🚀 Empaquetando SISFAC como paquete DEB para Kubuntu..."
echo ""

# Directorios
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$ROOT_DIR/venv"

# Paso 1: Compilar backend con PyInstaller
echo "📦 Paso 1: Compilando backend..."
cd "$ROOT_DIR/backend"

if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Instalar PyInstaller si no está
$PYTHON_CMD -c "import PyInstaller" 2>/dev/null || pip install pyinstaller

# Limpiar y compilar
rm -rf build/ dist/
export PYTHONHASHSEED=0
$PYTHON_CMD -m PyInstaller sisfac-backend.spec --clean --noconfirm

if [ ! -f "dist/sisfac-backend" ]; then
    echo "❌ Error: Backend no compilado"
    exit 1
fi

chmod +x dist/sisfac-backend
echo "✅ Backend compilado"
cd "$ROOT_DIR"

# Paso 2: Empaquetar con Electron
echo ""
echo "📦 Paso 2: Empaquetando con Electron..."
cd "$ROOT_DIR/electron"

# Verificar dependencias
command -v node >/dev/null || { echo "❌ Node.js requerido"; exit 1; }
[ ! -d "node_modules" ] && npm install

# Limpiar builds anteriores
rm -rf dist/linux-unpacked dist/*.AppImage 2>/dev/null || true

# Empaquetar (genera DEB para Kubuntu/Ubuntu)
npm run dist:deb

# Buscar archivo DEB generado
DEB=$(find dist -name "*.deb" -type f 2>/dev/null | head -1)

echo ""
if [ -n "$DEB" ]; then
    SIZE=$(du -h "$DEB" | cut -f1)
    echo "✅ ¡Empaquetado completado!"
    echo ""
    echo "📦 Paquete DEB (Kubuntu/Ubuntu):"
    echo "   Archivo: $DEB"
    echo "   Tamaño: $SIZE"
    echo ""
    echo "📥 Instalar:"
    echo "   sudo dpkg -i $DEB"
    echo "   # O"
    echo "   sudo apt install ./$DEB"
    echo ""
    echo "🗑️  Desinstalar:"
    echo "   sudo apt remove sisfac-desktop"
    echo ""
    echo "💡 Después de instalar, busca 'SISFAC' en el menú de aplicaciones"
    echo "💡 Paquete autónomo - NO requiere dependencias externas"
else
    echo "❌ Error: No se generó el paquete DEB"
    exit 1
fi
echo ""

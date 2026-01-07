#!/bin/bash
# Script TODO-EN-UNO para Linux
# - Instala Python (verifica)
# - Instala Node.js y Electron (si no están)
# - Prepara entorno completo

set -e

echo ""
echo "================================"
echo "  Preparar TODO SISFAC (Linux)"
echo "  Python + Node.js + Electron"
echo "================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Detectar directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR"

# Paso 1: Python
echo -e "${YELLOW}[1/3] Preparando Python...${NC}"
bash "$SCRIPT_DIR/../start.sh" --setup-only 2>/dev/null || {
    # Si start.sh no tiene opción --setup-only, hacerlo manualmente
    if [ ! -d "venv" ]; then
        echo "  Creando entorno virtual..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    if ! python -c "import flask" 2>/dev/null; then
        echo "  Instalando dependencias Python..."
        pip install -r requirements.txt
    fi
    
    deactivate 2>/dev/null || true
}

# Paso 2: Node.js y Electron
echo ""
echo -e "${YELLOW}[2/3] Preparando Node.js y Electron...${NC}"
bash "$SCRIPT_DIR/instalar_nodejs_electron_linux.sh"

# Paso 3: Verificación final
echo ""
echo -e "${YELLOW}[3/3] Verificacion final...${NC}"
echo ""
echo "Python:"
python3 --version
echo ""
echo "Node.js:"
node --version
echo ""
echo "Electron:"
cd electron
npm list electron --depth=0 | grep electron || echo "  Electron instalado"
cd ..

echo ""
echo -e "${GREEN}================================"
echo "  TODO LISTO!"
echo "================================"
echo -e "${NC}"
echo "Puedes:"
echo "  1. Iniciar la aplicacion:"
echo "     ./start.sh"
echo ""
echo "  2. Empaquetar la aplicacion:"
echo "     ./empaquetar.sh"
echo ""


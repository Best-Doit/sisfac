#!/bin/bash
# Script automatizado para instalar Node.js y Electron en Linux
# - Verifica/instala Node.js
# - Instala Electron y dependencias

set -e

echo ""
echo "================================"
echo "  Instalar Node.js y Electron"
echo "  (Linux - Automatizado)"
echo "================================"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detectar directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR"

# Paso 1: Verificar Node.js
echo -e "${YELLOW}[1/4] Verificando Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo "  Node.js no encontrado. Intentando instalar..."
    echo ""
    
    # Detectar distribución Linux
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        echo "  Detectado: Debian/Ubuntu"
        echo "  Instalando Node.js desde NodeSource..."
        
        # Verificar si tiene permisos sudo
        if ! sudo -n true 2>/dev/null; then
            echo -e "${RED}  ERROR: Se requieren permisos sudo para instalar Node.js${NC}"
            echo ""
            echo "  Por favor, ejecuta:"
            echo "    sudo bash scripts/instalar_nodejs_electron_linux.sh"
            exit 1
        fi
        
        # Instalar Node.js 20.x LTS desde NodeSource
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}  ERROR: Fallo la instalacion de Node.js${NC}"
            echo ""
            echo "  Intenta manualmente:"
            echo "    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -"
            echo "    sudo apt-get install -y nodejs"
            exit 1
        fi
        
        echo -e "${GREEN}  Node.js instalado correctamente${NC}"
    elif [ -f /etc/redhat-release ]; then
        # RedHat/CentOS/Fedora
        echo "  Detectado: RedHat/CentOS/Fedora"
        echo "  Instalando Node.js desde NodeSource..."
        
        if ! sudo -n true 2>/dev/null; then
            echo -e "${RED}  ERROR: Se requieren permisos sudo para instalar Node.js${NC}"
            exit 1
        fi
        
        curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
        sudo yum install -y nodejs
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}  ERROR: Fallo la instalacion de Node.js${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}  Node.js instalado correctamente${NC}"
    elif command -v pacman &> /dev/null; then
        # Arch Linux
        echo "  Detectado: Arch Linux"
        
        if ! sudo -n true 2>/dev/null; then
            echo -e "${RED}  ERROR: Se requieren permisos sudo para instalar Node.js${NC}"
            exit 1
        fi
        
        sudo pacman -S --noconfirm nodejs npm
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}  ERROR: Fallo la instalacion de Node.js${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}  Node.js instalado correctamente${NC}"
    else
        echo -e "${RED}  ERROR: Distribucion Linux no soportada automaticamente${NC}"
        echo ""
        echo "  Por favor, instala Node.js manualmente:"
        echo "    Visita: https://nodejs.org/"
        echo "    O usa el gestor de paquetes de tu distribucion"
        exit 1
    fi
else
    echo -e "${GREEN}  Node.js encontrado:${NC}"
    node --version
fi

# Paso 2: Verificar npm
echo ""
echo -e "${YELLOW}[2/4] Verificando npm...${NC}"
if ! command -v npm &> /dev/null; then
    echo -e "${RED}  ERROR: npm no encontrado. Reinstala Node.js${NC}"
    exit 1
fi
echo -e "${GREEN}  npm encontrado:${NC}"
npm --version

# Paso 3: Verificar/instalar Node.js versión mínima
echo ""
echo -e "${YELLOW}[3/4] Verificando version de Node.js...${NC}"
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${YELLOW}  Advertencia: Se recomienda Node.js 18 o superior${NC}"
    echo "  Version actual: $(node --version)"
fi

# Paso 4: Instalar Electron
echo ""
echo -e "${YELLOW}[4/4] Instalando Electron y dependencias...${NC}"
cd electron

if [ ! -d "node_modules" ]; then
    echo "  Instalando dependencias de Electron..."
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}  ERROR: Fallo la instalacion de Electron${NC}"
        echo "  Intenta manualmente: cd electron && npm install"
        exit 1
    fi
else
    echo "  Verificando dependencias de Electron..."
    if ! npm list electron >/dev/null 2>&1; then
        echo "  Instalando dependencias faltantes..."
        npm install
    else
        echo -e "${GREEN}  Electron ya esta instalado${NC}"
    fi
fi

# Verificar instalación
echo ""
echo "Verificando instalacion..."
npm list electron --depth=0
npm list electron-builder --depth=0

if [ $? -ne 0 ]; then
    echo -e "${RED}  ERROR: Electron no se instalo correctamente${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}================================"
echo "  Instalacion completada!"
echo "================================"
echo -e "${NC}"
echo "Node.js:"
node --version
echo "npm:"
npm --version
echo "Electron:"
npm list electron --depth=0 | grep electron
echo "electron-builder:"
npm list electron-builder --depth=0 | grep electron-builder
echo ""
echo "Puedes empaquetar la aplicacion con:"
echo "  ./empaquetar.sh"
echo ""

cd "$ROOT_DIR"


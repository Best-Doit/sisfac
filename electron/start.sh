#!/bin/bash
# Script para iniciar Electron sin problemas de sandbox

cd "$(dirname "$0")"

# Deshabilitar sandbox mediante variable de entorno
export ELECTRON_DISABLE_SANDBOX=1

# Iniciar Electron
npm start


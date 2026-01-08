# SISFAC - Sistema de Facturación

Sistema de facturación de escritorio (interfaz web embebida) para pequeños negocios.  
Construido con Flask, Tailwind CSS, Alpine.js y Electron.

## 🚀 Características

- ✅ Gestión de clientes, inventario y facturación
- ✅ Múltiples precios por producto (Principal, P1, P2)
- ✅ Dashboard con métricas
- ✅ Sistema de backups y restauración
- ✅ Importación masiva desde Excel
- ✅ Búsqueda predictiva
- ✅ Interfaz moderna y responsive

## 📋 Requisitos

- Python 3.9+ (recomendado: 3.12)
- Node.js y npm (para empaquetado)

## 🔧 Instalación

Los scripts automatizados instalan todas las dependencias necesarias en el proyecto, incluso si ya están instaladas en el sistema.

### 🐧 Linux

**Instalación completa (recomendado):**
```bash
bash scripts/preparar_todo_linux.sh
```
Este script instala y configura automáticamente:
- ✅ Python y entorno virtual (`venv`)
- ✅ Todas las dependencias de Python (Flask, SQLAlchemy, etc.)
- ✅ Node.js (si no está instalado, requiere sudo)
- ✅ Electron y electron-builder en el proyecto

**Iniciar aplicación:**
```bash
./start.sh
```

**Empaquetar aplicación:**
```bash
./empaquetar.sh
```

## 📦 Scripts Disponibles

### Linux

**Scripts de instalación:**
- `scripts/preparar_todo_linux.sh` - **Todo en uno**: Instala Python, Node.js y Electron
- `scripts/instalar_nodejs_electron_linux.sh` - Solo Node.js (si falta) y Electron en el proyecto

**Scripts de uso:**
- `./start.sh` - Crea venv (si no existe), instala dependencias e inicia la aplicación
- `./empaquetar.sh` - Compila backend con PyInstaller y empaqueta con Electron

**Nota:** Los scripts siempre instalan las dependencias en el proyecto, incluso si ya están instaladas en el sistema.

## 🎯 Uso Rápido

1. **Preparar entorno:** Ejecuta el script "todo en uno"
   ```bash
   bash scripts/preparar_todo_linux.sh
   ```
   
2. **Iniciar aplicación:**
   ```bash
   ./start.sh
   ```
   
3. **Acceder:** Abre `http://localhost:5000` en tu navegador

**Importante:** Los scripts instalan todas las dependencias necesarias en el proyecto. No necesitas tener Python o Node.js instalados globalmente (aunque ayuda para la primera instalación de Node.js).

## 📁 Estructura

```
SISFAC/
├── backend/          # Backend Flask
├── electron/         # Aplicación Electron
├── scripts/          # Scripts automatizados
├── documentacion/    # Documentación completa
└── requirements.txt   # Dependencias Python
```

## 📚 Documentación

Toda la documentación está en el directorio [`documentacion/`](./documentacion/):

- [📖 Índice de Documentación](./documentacion/README.md) - Guía completa
- [🏗️ Arquitectura Técnica](./documentacion/ARQUITECTURA_TECNICA.md) - Estructura del sistema
- [📦 Guía de Empaquetado](./documentacion/EMPAQUETADO.md) - Crear ejecutables
- [🔒 Empaquetado Seguro](./documentacion/EMPAQUETADO_SEGURO.md) - Protección de datos
- [📝 Cambios Recientes](./documentacion/CAMBIOS_RECIENTES.md) - Últimas actualizaciones

## 📄 Licencia

**Uso no comercial**

Permisos: Ver, estudiar, usar para fines personales/educativos, modificar y compartir con atribución.  
Restricciones: No se permite uso comercial sin autorización.

## 👤 Créditos

**Desarrollado por:** Best_Doit  
**TikTok:** [@best_doit](https://www.tiktok.com/@best_doit)

---

## ⚠️ Disclaimer

Este software se proporciona "tal cual", sin garantías de ningún tipo.

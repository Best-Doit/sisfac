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

### 🪟 Windows

**Todo en uno (recomendado):**
```cmd
scripts\preparar_todo_windows.bat
```

**Iniciar aplicación:**
```cmd
venv\Scripts\activate
cd backend
python run.py
```

**Empaquetar:**
```cmd
scripts\empaquetar_windows.bat
```

### 🐧 Linux

**Todo en uno (recomendado):**
```bash
bash scripts/preparar_todo_linux.sh
```

**Iniciar aplicación:**
```bash
./start.sh
```

**Empaquetar:**
```bash
./empaquetar.sh
```

## 📦 Scripts Disponibles

### Windows
- `scripts\preparar_todo_windows.bat` - Instala todo (Python + Node.js + Electron)
- `scripts\preparar_entorno_windows.bat` - Solo Python
- `scripts\instalar_nodejs_electron_windows.bat` - Solo Node.js y Electron
- `scripts\empaquetar_windows.bat` - Empaquetar aplicación

### Linux
- `scripts/preparar_todo_linux.sh` - Instala todo (Python + Node.js + Electron)
- `scripts/instalar_nodejs_electron_linux.sh` - Solo Node.js y Electron
- `./start.sh` - Iniciar aplicación
- `./empaquetar.sh` - Empaquetar aplicación

## 🎯 Uso Rápido

1. **Preparar entorno:** Ejecuta el script "todo en uno" de tu sistema
2. **Iniciar:** Usa `./start.sh` (Linux) o activa venv y ejecuta `python run.py` (Windows)
3. **Acceder:** Abre `http://localhost:5000` en tu navegador

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

- [Documentación Técnica](./documentacion/README.md)
- [Cambios Recientes](./documentacion/CAMBIOS_RECIENTES.md)
- [Arquitectura Técnica](./documentacion/ARQUITECTURA_TECNICA.md)

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

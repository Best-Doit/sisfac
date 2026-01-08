# 📦 Guía de Empaquetado - SISFAC

## 🔒 Protección de Datos de Producción

**⚠️ IMPORTANTE:** Los datos de producción están en `~/.sisfac/` y **NUNCA se tocan** durante el empaquetado.

- ✅ El empaquetado solo incluye **código**
- ✅ Los datos en `~/.sisfac/sisfac.db` **nunca se modifican**
- ✅ Las actualizaciones solo cambian código, no datos

Ver detalles completos en: [Empaquetado Seguro - Protección de Datos](./EMPAQUETADO_SEGURO.md)

---

## 🚀 Empaquetado Rápido

### Usando el Script Automatizado (Recomendado)

```bash
./empaquetar.sh
```

Este script:
1. Compila el backend con PyInstaller
2. Empaqueta todo con Electron
3. Genera `electron/dist/SISFAC-1.0.0.AppImage`

### Empaquetado Manual

```bash
# 1. Compilar backend
cd backend
source ../venv/bin/activate
pyinstaller sisfac-backend.spec

# 2. Empaquetar con Electron
cd ../electron
npm run dist
```

---

## 📋 Requisitos Previos

- ✅ Python 3.9+ con entorno virtual (`venv`)
- ✅ Node.js y npm
- ✅ PyInstaller instalado: `pip install pyinstaller`
- ✅ electron-builder instalado: `npm install` (en `electron/`)

---

## 🔧 Configuración

### Archivos Incluidos en el AppImage

- ✅ Backend compilado (`backend/dist/sisfac-backend`)
- ✅ Código de Electron (`main.js`, `preload.js`)
- ⚠️ Base de datos inicial (opcional, solo para primera ejecución)
- ⚠️ Backups iniciales (opcional, solo para primera ejecución)

### Ubicación de Datos

**En Producción:**
- Base de datos: `~/.sisfac/sisfac.db`
- Backups: `~/.sisfac/backups/`

**En Desarrollo:**
- Base de datos: `./sisfac.db`
- Backups: `./backups/`

---

## 🚀 Ejecutar el AppImage

### Opción 1: Script Wrapper (Recomendado)

```bash
cd electron
./ejecutar_appimage.sh ./dist/SISFAC-1.0.0.AppImage
```

### Opción 2: Ejecución Directa

```bash
cd electron/dist
chmod +x SISFAC-1.0.0.AppImage
ELECTRON_DISABLE_SANDBOX=1 ./SISFAC-1.0.0.AppImage --no-sandbox
```

---

## 🔍 Verificación

Después de empaquetar:

```bash
# 1. Verificar que el AppImage se creó
ls -lh electron/dist/SISFAC-*.AppImage

# 2. Verificar que los datos de producción siguen intactos
ls -lh ~/.sisfac/sisfac.db

# 3. Ejecutar el nuevo AppImage
cd electron
./ejecutar_appimage.sh ./dist/SISFAC-1.0.0.AppImage
```

---

## 🐛 Solución de Problemas

### Error: "Backend no encontrado"
- Verifica que `backend/dist/sisfac-backend` existe
- Ejecuta `./empaquetar.sh` completo

### Error: "Permission denied"
```bash
chmod +x electron/dist/SISFAC-1.0.0.AppImage
```

### Error: "Database not found"
- Normal en primera ejecución
- La app creará la base de datos en `~/.sisfac/`

### AppImage no inicia
- Usa el script wrapper: `./ejecutar_appimage.sh`
- O ejecuta con: `ELECTRON_DISABLE_SANDBOX=1 ./AppImage --no-sandbox`

---

## 📝 Notas Importantes

1. **Primera ejecución**: Puede tardar 2-5 segundos en iniciar
2. **Base de datos**: Se crea automáticamente en `~/.sisfac/` si no existe
3. **Puerto**: La aplicación usa `http://127.0.0.1:5000`
4. **Tamaño**: ~100-200MB (incluye Electron + Python empaquetado)
5. **Independencia**: No requiere Python ni Node.js instalados en el sistema destino

---

## 📚 Documentación Relacionada

- [Empaquetado Seguro - Protección de Datos](./EMPAQUETADO_SEGURO.md) - Detalles sobre protección de datos
- [Arquitectura Técnica](./ARQUITECTURA_TECNICA.md) - Estructura del sistema
- [Guía de Desarrollo](./guia_desarrollo/README.md) - Desarrollo y contribución


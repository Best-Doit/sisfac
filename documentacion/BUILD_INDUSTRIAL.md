# 🏭 Build Industrial - AppImage Autónomo

## 📋 Resumen Ejecutivo

Este documento describe el proceso de build para generar un **AppImage completamente autónomo** que no requiere:
- ❌ Python instalado
- ❌ Node.js instalado
- ❌ Librerías del sistema
- ❌ Dependencias externas

El AppImage resultante es **portable, reproducible y listo para distribución comercial**.

---

## 🎯 Objetivos del Build

1. ✅ **Autonomía total**: Sin dependencias del sistema
2. ✅ **Portabilidad**: Funciona en cualquier Linux moderno (x64)
3. ✅ **Reproducibilidad**: Builds consistentes y determinísticos
4. ✅ **Optimización**: Tamaño mínimo sin sacrificar funcionalidad
5. ✅ **Robustez**: Manejo de errores y cierre graceful

---

## 🏗️ Arquitectura del Build

```
SISFAC/
├── backend/                    # Backend Flask
│   ├── run.py                  # Punto de entrada
│   ├── sisfac-backend.spec     # Config PyInstaller (--onefile)
│   └── app/                    # Código de la aplicación
│       ├── __init__.py
│       ├── config.py           # Rutas dinámicas (sin hardcodes)
│       ├── models.py
│       ├── routes/
│       └── services/
│
├── electron/                   # Frontend Electron
│   ├── main.js                 # Proceso principal (inicia backend)
│   ├── preload.js              # Script de preload (seguridad)
│   ├── package.json            # Config electron-builder
│   └── build/
│       ├── afterPack.js        # Hook post-packaging
│       └── afterAllArtifactBuild.js  # Hook post-AppImage
│
└── empaquetar.sh               # Script de build automatizado
```

---

## 📦 Configuración PyInstaller (Backend)

### Archivo: `backend/sisfac-backend.spec`

**Características clave:**
- ✅ Modo `--onefile`: Un solo ejecutable
- ✅ Optimización nivel 2: Balance tamaño/velocidad
- ✅ Stripping de símbolos: Reduce tamaño
- ✅ UPX compression: Comprime el binario
- ✅ Exclusión de módulos innecesarios: Reduce tamaño

**Ubicación del ejecutable generado:**
```
backend/dist/sisfac-backend
```

**Tamaño esperado:** ~50-80 MB (depende de dependencias)

---

## ⚙️ Configuración electron-builder (Frontend)

### Archivo: `electron/package.json`

**Configuración clave:**

```json
{
  "build": {
    "compression": "maximum",      // Máxima compresión
    "asar": true,                  // Empaquetar en ASAR
    "extraResources": [
      {
        "from": "../backend/dist/sisfac-backend",
        "to": "backend/sisfac-backend"  // ⚠️ Nueva ubicación optimizada
      }
    ],
    "appImage": {
      "artifactName": "${productName}-${version}.${ext}"
    }
  }
}
```

**Cambios importantes:**
- ✅ Ejecutable backend en `backend/sisfac-backend` (no en `backend/dist/`)
- ✅ Compresión máxima activada
- ✅ Archivos innecesarios excluidos

---

## 🔧 Configuración main.js (Electron)

### Cambios Implementados

1. **Detección de ruta del backend:**
   ```javascript
   backendExecutable = path.join(resourcesPath, 'backend', 'sisfac-backend');
   ```

2. **Manejo robusto de errores:**
   - Verificación de existencia del ejecutable
   - Establecimiento de permisos automático
   - Manejo de cierre graceful del backend

3. **Cierre graceful:**
   - SIGTERM primero (3 segundos)
   - SIGKILL si no responde

---

## 🚀 Proceso de Build

### Paso 1: Compilar Backend

```bash
cd backend
source ../venv/bin/activate
pyinstaller sisfac-backend.spec
```

**Resultado:** `backend/dist/sisfac-backend`

### Paso 2: Empaquetar con Electron

```bash
cd electron
npm run dist
```

**Resultado:** `electron/dist/SISFAC-1.0.0.AppImage`

### Script Automatizado

```bash
./empaquetar.sh
```

Este script:
1. ✅ Verifica dependencias
2. ✅ Compila backend con PyInstaller
3. ✅ Filtra archivos opcionales dinámicamente
4. ✅ Empaqueta con electron-builder
5. ✅ Configura AppRun para doble clic
6. ✅ Verifica el resultado

---

## 📊 Estructura Final del AppImage

```
SISFAC-1.0.0.AppImage (squashfs)
├── AppRun                      # Script de ejecución (con flags sandbox)
├── sisfac-desktop              # Binario Electron
├── resources/
│   ├── app.asar                # Código Electron empaquetado
│   ├── backend/
│   │   └── sisfac-backend      # Backend Flask (PyInstaller --onefile)
│   ├── sisfac.db               # Base de datos inicial (opcional)
│   ├── backups/                # Directorio de backups (opcional)
│   └── icon.png                # Icono de la aplicación
└── usr/                        # Metadatos AppImage
    └── share/
        └── applications/
            └── SISFAC.desktop
```

---

## 🔒 Rutas y Datos

### Rutas Dinámicas (Sin Hardcodes)

**Backend (`app/config.py`):**
- ✅ Detecta si está empaquetado: `sys.frozen`
- ✅ Usa `~/.sisfac/` para datos de producción
- ✅ Copia datos iniciales solo si no existen datos de producción

**Electron (`main.js`):**
- ✅ Usa `process.resourcesPath` (no hardcoded)
- ✅ Detecta modo desarrollo vs. empaquetado

### Ubicación de Datos

**Producción (empaquetado):**
- Base de datos: `~/.sisfac/sisfac.db`
- Backups: `~/.sisfac/backups/`

**Desarrollo:**
- Base de datos: `./sisfac.db`
- Backups: `./backups/`

**⚠️ IMPORTANTE:** Los datos en `~/.sisfac/` **NUNCA** se tocan durante actualizaciones.

---

## 🎯 Optimizaciones Aplicadas

### Backend (PyInstaller)

1. ✅ **Exclusión de módulos innecesarios:**
   - matplotlib, numpy, pandas, scipy
   - tkinter, pydoc, unittest
   - setuptools, distutils

2. ✅ **Optimización nivel 2:**
   - Balance entre tamaño y velocidad

3. ✅ **Stripping y UPX:**
   - Reduce tamaño del binario

### Frontend (Electron)

1. ✅ **Compresión máxima:**
   - ASAR con compresión

2. ✅ **Exclusión de archivos:**
   - node_modules innecesarios
   - Archivos de desarrollo
   - Documentación

3. ✅ **Estructura optimizada:**
   - Ejecutable backend directamente en `backend/`

---

## 🐛 Errores Comunes y Soluciones

### Error: "Backend executable not found"

**Causa:** El ejecutable no está en la ubicación esperada.

**Solución:**
1. Verificar que PyInstaller generó `backend/dist/sisfac-backend`
2. Verificar que `package.json` tiene la ruta correcta en `extraResources`
3. Ejecutar `./empaquetar.sh` completo

### Error: "Permission denied"

**Causa:** El ejecutable no tiene permisos de ejecución.

**Solución:**
- El hook `afterPack.js` debería establecerlos automáticamente
- Si falla, verificar permisos del sistema de archivos

### Error: AppImage no ejecuta con doble clic

**Causa:** AppRun no tiene los flags de sandbox.

**Solución:**
- El hook `afterAllArtifactBuild.js` debería modificarlo automáticamente
- Verificar que `mksquashfs` está instalado

### Error: Backend se cierra inesperadamente

**Causa:** Error en el backend o dependencia faltante.

**Solución:**
1. Verificar logs del backend (en consola)
2. Probar el ejecutable directamente: `./backend/dist/sisfac-backend`
3. Verificar que todas las dependencias están en `hiddenimports`

---

## 📏 Tamaños Esperados

- **Backend (sisfac-backend):** ~50-80 MB
- **Electron bundle:** ~100-120 MB
- **AppImage final:** ~120-150 MB

**Optimizaciones futuras:**
- Usar Electron más reciente (puede ser más pequeño)
- Tree-shaking de dependencias Python
- Comprimir más agresivamente

---

## 🔄 Build Reproducible

### Variables de Entorno

```bash
export PYTHONHASHSEED=0          # Para builds determinísticos
export SOURCE_DATE_EPOCH=$(date +%s)  # Timestamp fijo
```

### Dependencias Fijas

- Python: 3.12.3
- Electron: 28.0.0
- electron-builder: 24.13.3
- PyInstaller: 6.17.0

---

## ✅ Checklist de Build

Antes de distribuir:

- [ ] Backend compila sin errores
- [ ] Ejecutable backend funciona standalone
- [ ] AppImage se genera correctamente
- [ ] AppImage ejecuta con doble clic
- [ ] Backend inicia automáticamente
- [ ] Backend se cierra correctamente
- [ ] Datos se guardan en `~/.sisfac/`
- [ ] No hay dependencias del sistema
- [ ] Tamaño del AppImage es razonable
- [ ] Icono se muestra correctamente
- [ ] AppImage funciona en sistema limpio (sin Python/Node)

---

## 🚀 Distribución

### Verificación Final

```bash
# 1. Verificar que el AppImage es ejecutable
chmod +x electron/dist/SISFAC-1.0.0.AppImage

# 2. Probar ejecución
./electron/dist/SISFAC-1.0.0.AppImage

# 3. Verificar tamaño
ls -lh electron/dist/SISFAC-1.0.0.AppImage

# 4. Verificar contenido
./electron/dist/SISFAC-1.0.0.AppImage --appimage-extract
ls -la squashfs-root/resources/backend/
```

### Distribución

1. **Subir a servidor de releases**
2. **Verificar checksums (SHA256)**
3. **Probar en sistema limpio**
4. **Documentar requisitos mínimos:**
   - Linux x64
   - Kernel 3.10+ (para AppImage)
   - FUSE (para montar AppImage)

---

## 📚 Referencias

- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [electron-builder Documentation](https://www.electron.build/)
- [AppImage Specification](https://docs.appimage.org/)

---

**Última actualización:** 2026-02-03
**Versión del build:** 5.6.0

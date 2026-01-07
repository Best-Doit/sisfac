# Guía de Empaquetado - SISFAC

Esta guía explica cómo empaquetar SISFAC en una aplicación ejecutable única.

## 📦 Opciones de Empaquetado

### Opción 1: Empaquetado Simple (Recomendado para desarrollo)

Empaqueta Electron con el backend Flask como archivos Python. Requiere que el usuario tenga Python instalado.

#### Linux (AppImage)
```bash
cd electron
npm run build:linux
```

El ejecutable se generará en `electron/dist/SISFAC-1.0.0.AppImage`

#### Windows
```bash
cd electron
npm run build:win
```

El instalador se generará en `electron/dist/SISFAC Setup 1.0.0.exe`

#### macOS
```bash
cd electron
npm run build:mac
```

El archivo DMG se generará en `electron/dist/SISFAC-1.0.0.dmg`

---

### Opción 2: Empaquetado Completo (Recomendado para distribución)

Empaqueta Python junto con la aplicación usando PyInstaller.

#### Paso 1: Empaquetar el backend Flask con PyInstaller

1. Instalar PyInstaller:
```bash
cd ..
source venv/bin/activate
pip install pyinstaller
```

2. Crear el ejecutable del backend:
```bash
cd backend
pyinstaller --onefile --name sisfac-backend --add-data "app:app" run.py
```

3. El ejecutable se generará en `backend/dist/sisfac-backend`

#### Paso 2: Actualizar main.js para usar el ejecutable

Modificar `electron/main.js` para usar el ejecutable en lugar de Python:
```javascript
const backendExecutable = path.join(projectRoot, 'backend', 'dist', 'sisfac-backend');
backendProcess = spawn(backendExecutable, [], {
  cwd: projectRoot,
  // ...
});
```

#### Paso 3: Empaquetar con Electron

```bash
cd electron
npm run build
```

---

## 🚀 Empaquetado Rápido (Linux)

Para crear un AppImage ejecutable:

```bash
cd electron
npm run dist
```

El archivo `SISFAC-1.0.0.AppImage` estará en `electron/dist/`

Para ejecutarlo:
```bash
chmod +x dist/SISFAC-1.0.0.AppImage
./dist/SISFAC-1.0.0.AppImage
```

---

## 📋 Requisitos Previos

1. **Node.js y npm** instalados
2. **electron-builder** instalado (ya está en package.json)
3. **Python 3.9+** (para la opción 1)
4. **PyInstaller** (solo para la opción 2)

---

## ⚙️ Configuración Actual

La configuración en `package.json` incluye:

- **Linux**: AppImage y .deb
- **Windows**: Instalador NSIS
- **macOS**: DMG

Los archivos incluidos:
- Backend Flask completo
- Base de datos (sisfac.db)
- Backups (directorio)
- main.js y package.json

---

## 🔧 Solución de Problemas

### Error: "Cannot find module"
- Asegúrate de que todas las dependencias estén instaladas: `npm install`

### Error: "Python not found"
- Para la opción 1: Instala Python 3.9+ en el sistema
- Para la opción 2: Usa PyInstaller para empaquetar Python

### Error: "Database not found"
- El archivo `sisfac.db` se copia automáticamente a `extraResources`
- Verifica que exista en la raíz del proyecto

---

## 📝 Notas Importantes

1. **Primera ejecución**: La aplicación creará la base de datos si no existe
2. **Backups**: Se guardan en el directorio `backups/` relativo al ejecutable
3. **Tamaño**: El AppImage será grande (~100-200MB) porque incluye Electron y el backend
4. **Python**: La opción 1 requiere Python instalado en el sistema destino

---

## 🎯 Recomendación

Para distribución final, usa la **Opción 2** (PyInstaller + Electron) para crear un ejecutable completamente independiente que no requiera Python instalado.

Para desarrollo y pruebas rápidas, usa la **Opción 1** (solo Electron).


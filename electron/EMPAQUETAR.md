# 🚀 Guía de Empaquetado - SISFAC

## Empaquetado Rápido (Linux - AppImage)

Para crear un ejecutable AppImage:

```bash
cd electron
npm run dist
```

El archivo se generará en: `electron/dist/SISFAC-1.0.0.AppImage`

Para ejecutarlo:
```bash
chmod +x dist/SISFAC-1.0.0.AppImage
./dist/SISFAC-1.0.0.AppImage
```

---

## 📦 Opciones de Empaquetado

### Linux (AppImage)
```bash
cd electron
npm run build
```

Genera:
- `SISFAC-1.0.0.AppImage` (ejecutable portable)

---

## ⚠️ Requisitos Importantes

### Para el Ejecutable Funcione:

1. **Python 3.9+ debe estar instalado** en el sistema destino
2. **Dependencias Python** deben estar instaladas:
   ```bash
   pip install -r requirements.txt
   ```

### Alternativa: Empaquetado Completo (Sin Python Requerido)

Para crear un ejecutable que NO requiera Python instalado, necesitas empaquetar el backend con PyInstaller primero:

#### Paso 1: Empaquetar Backend con PyInstaller

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar PyInstaller
pip install pyinstaller

# Empaquetar backend
cd backend
pyinstaller --onefile --name sisfac-backend --add-data "app:app" run.py
```

Esto creará `backend/dist/sisfac-backend`

#### Paso 2: Actualizar main.js

Modificar `electron/main.js` para usar el ejecutable:

```javascript
if (isPackaged) {
  const backendExecutable = path.join(process.resourcesPath, 'app.asar.unpacked', 'backend', 'dist', 'sisfac-backend');
  backendProcess = spawn(backendExecutable, [], {
    // ...
  });
}
```

#### Paso 3: Actualizar package.json

Agregar el ejecutable a `extraResources`:

```json
"extraResources": [
  {
    "from": "../backend/dist/sisfac-backend",
    "to": "backend/dist/sisfac-backend"
  }
]
```

#### Paso 4: Empaquetar con Electron

```bash
cd electron
npm run build
```

---

## 📋 Archivos Incluidos en el Empaquetado

- ✅ Backend Flask completo (`backend/`)
- ✅ Base de datos (`sisfac.db`)
- ✅ Directorio de backups (`backups/`)
- ✅ `main.js` y `package.json`
- ❌ `node_modules/` (excluido, se empaqueta por separado)
- ❌ `venv/` (no se incluye, requiere Python del sistema)

---

## 🔧 Solución de Problemas

### Error: "Python not found"
- **Solución 1**: Instala Python 3.9+ en el sistema
- **Solución 2**: Usa PyInstaller para empaquetar Python (ver arriba)

### Error: "Module not found"
- Ejecuta `pip install -r requirements.txt` en el entorno virtual
- Asegúrate de que todas las dependencias estén instaladas

### Error: "Database not found"
- El archivo `sisfac.db` se copia automáticamente
- Si no existe, la app lo creará en el primer uso

### AppImage no se ejecuta
```bash
chmod +x SISFAC-1.0.0.AppImage
./SISFAC-1.0.0.AppImage
```

---

## 📝 Notas

- **Tamaño del ejecutable**: ~100-200MB (incluye Electron)
- **Primera ejecución**: Puede tardar unos segundos en iniciar
- **Base de datos**: Se crea automáticamente si no existe
- **Backups**: Se guardan en `backups/` relativo al ejecutable

---

## 🎯 Recomendación

Para **distribución final**, usa PyInstaller + Electron para crear un ejecutable completamente independiente.

Para **pruebas rápidas**, el empaquetado simple funciona bien si el sistema destino tiene Python instalado.


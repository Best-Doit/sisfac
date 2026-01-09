// CRÍTICO: Deshabilitar sandbox ANTES de importar 'electron'
// Esto debe ejecutarse antes de cualquier otra inicialización
process.env.ELECTRON_DISABLE_SANDBOX = '1';

const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

// Deshabilitar sandbox para evitar problemas de permisos
// IMPORTANTE: Debe ejecutarse ANTES de que app esté listo
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('--disable-setuid-sandbox');
app.commandLine.appendSwitch('--disable-zygote');

let mainWindow = null;
let backendProcess = null;
let appIsQuitting = false;

function startBackend() {
  const fs = require('fs');
  
  // Detectar si estamos en modo desarrollo o empaquetado
  const isPackaged = app.isPackaged;
  
  let backendExecutable, projectRoot;
  
  if (isPackaged) {
    // Modo empaquetado: usar el ejecutable de PyInstaller
    // El ejecutable está en extraResources/backend/
    const resourcesPath = process.resourcesPath;
    backendExecutable = path.join(resourcesPath, 'backend', 'sisfac-backend');
    projectRoot = resourcesPath;
    
    // Verificar que el ejecutable existe
    if (!fs.existsSync(backendExecutable)) {
      dialog.showErrorBox('Error Crítico', 
        `No se encontró el ejecutable del backend.\n\n` +
        `Buscado en: ${backendExecutable}\n\n` +
        `El AppImage está corrupto o incompleto.\n` +
        `Por favor, reinstale la aplicación.`
      );
      app.quit();
      return;
    }
    
    // Los permisos se establecen en postinst.sh durante la instalación
    // No intentar chmod aquí porque requiere permisos root
  } else {
    // Modo desarrollo: usar Python del venv
    projectRoot = path.join(__dirname, '..');
    const backendScript = path.join(projectRoot, 'backend', 'run.py');
    const venvPython = path.join(projectRoot, 'venv', 'bin', 'python');
    const pythonCmd = fs.existsSync(venvPython) ? venvPython : 'python3';
    
    if (!fs.existsSync(backendScript)) {
      dialog.showErrorBox('Error', 
        `No se encontró el script del backend.\n\n` +
        `Buscado en: ${backendScript}`
      );
      app.quit();
      return;
    }
    
    backendProcess = spawn(pythonCmd, [backendScript], {
      cwd: projectRoot,
      env: {
        ...process.env,
        FLASK_ENV: 'development',
        FLASK_DEBUG: '1'
      },
      stdio: 'inherit'
    });

    backendProcess.on('error', (err) => {
      dialog.showErrorBox('Error iniciando backend', 
        `No se pudo iniciar el servidor Flask.\n\n` +
        `Error: ${err.message}\n\n` +
        `Asegúrate de tener Python 3.9+ instalado y las dependencias instaladas.`
      );
      app.quit();
    });
    
    backendProcess.on('exit', (code) => {
      if (code !== 0 && code !== null) {
        console.error(`Backend terminó con código: ${code}`);
      }
    });
    
    return;
  }

  // Ejecutar el backend empaquetado (sin argumentos, es un ejecutable)
  backendProcess = spawn(backendExecutable, [], {
    cwd: projectRoot,
    env: {
      ...process.env,
      FLASK_ENV: 'production',
      FLASK_DEBUG: '0',
      PYTHONUNBUFFERED: '1'  // Para logs en tiempo real
    },
    stdio: 'pipe'  // Cambiar a 'pipe' para capturar logs si es necesario
  });

  backendProcess.on('error', (err) => {
    dialog.showErrorBox('Error Crítico', 
      `No se pudo iniciar el servidor Flask.\n\n` +
      `Error: ${err.message}\n\n` +
      `Ejecutable: ${backendExecutable}\n\n` +
      `El AppImage puede estar corrupto.`
    );
    app.quit();
  });
  
  backendProcess.on('exit', (code, signal) => {
      if (code !== 0 && code !== null) {
        console.error(`Backend terminó inesperadamente. Código: ${code}, Señal: ${signal}`);
        if (!appIsQuitting) {
          dialog.showErrorBox('Error', 
            `El servidor Flask se detuvo inesperadamente.\n\n` +
            `Código de salida: ${code}\n\n` +
            `La aplicación se cerrará.`
          );
          app.quit();
        }
      }
  });
  
  // Capturar stderr para debugging (opcional, comentar en producción final)
  backendProcess.stderr.on('data', (data) => {
    const error = data.toString();
    if (error.includes('ERROR') || error.includes('CRITICAL')) {
      console.error(`Backend error: ${error}`);
    }
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // Cargar la app Flask
  mainWindow.loadURL('http://127.0.0.1:5000/');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startBackend();

  // Esperar a que arranque Flask y luego abrir la ventana
  // Intentar conectar hasta 10 veces (10 segundos máximo)
  let attempts = 0;
  const maxAttempts = 10;
  
  const tryConnect = () => {
    const req = http.get('http://127.0.0.1:5000/', (res) => {
      if (res.statusCode === 200 || res.statusCode === 302) {
        createWindow();
      } else {
        attempts++;
        if (attempts < maxAttempts) {
          setTimeout(tryConnect, 1000);
        } else {
          dialog.showErrorBox('Error', 
            'No se pudo conectar al servidor Flask.\n\n' +
            'Por favor, verifica que el backend se inició correctamente.'
          );
        }
      }
    });
    
    req.on('error', () => {
      attempts++;
      if (attempts < maxAttempts) {
        setTimeout(tryConnect, 1000);
      } else {
        dialog.showErrorBox('Error', 
          'No se pudo iniciar el servidor Flask.\n\n' +
          'El backend no respondió después de varios intentos.'
        );
      }
    });
    
    req.setTimeout(500, () => {
      req.destroy();
      attempts++;
      if (attempts < maxAttempts) {
        setTimeout(tryConnect, 1000);
      }
    });
  };
  
  // Iniciar intentos de conexión después de 1 segundo
  setTimeout(tryConnect, 1000);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  app.quit();
});

app.on('will-quit', (event) => {
  appIsQuitting = true;
  if (backendProcess) {
    console.log('Cerrando backend...');
    // Intentar cierre graceful primero
    backendProcess.kill('SIGTERM');
    
    // Si no responde en 3 segundos, forzar cierre
    setTimeout(() => {
      if (backendProcess && !backendProcess.killed) {
        console.log('Forzando cierre del backend...');
        backendProcess.kill('SIGKILL');
      }
    }, 3000);
    
    backendProcess = null;
  }
});

// Manejar cierre de ventana
app.on('before-quit', (event) => {
  appIsQuitting = true;
});

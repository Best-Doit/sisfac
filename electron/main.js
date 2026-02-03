// CRÍTICO: Deshabilitar sandbox ANTES de importar 'electron'
// Esto debe ejecutarse antes de cualquier otra inicialización
process.env.ELECTRON_DISABLE_SANDBOX = '1';

const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');
const net = require('net');

// Deshabilitar sandbox para evitar problemas de permisos
// IMPORTANTE: Debe ejecutarse ANTES de que app esté listo
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('--disable-setuid-sandbox');
app.commandLine.appendSwitch('--disable-zygote');

let mainWindow = null;
let backendProcess = null;
let appIsQuitting = false;
let backendPort = null;

if (process.platform === 'win32') {
  // Asegura icono correcto en barra de tareas y notificaciones
  app.setAppUserModelId('com.sisfac.desktop');
}

function getAppIconPath() {
  const isWindows = process.platform === 'win32';
  const isLinux = process.platform === 'linux';
  const iconName = isWindows ? 'icon.ico' : 'icon.png';

  if (app.isPackaged) {
    return path.join(process.resourcesPath, iconName);
  }

  if (isWindows) {
    return path.join(__dirname, 'build', 'icon.ico');
  }
  if (isLinux) {
    return path.join(__dirname, 'build', 'icon.png');
  }
  return undefined;
}

function getAvailablePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.unref();
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      server.close(() => resolve(port));
    });
  });
}

function startBackend(port) {
  const fs = require('fs');
  
  // Detectar si estamos en modo desarrollo o empaquetado
  const isPackaged = app.isPackaged;
  
  let backendExecutable, projectRoot;
  
  if (isPackaged) {
    // Modo empaquetado: usar el ejecutable de PyInstaller
    // El ejecutable está en extraResources/backend/
    const resourcesPath = process.resourcesPath;
    const isWindows = process.platform === 'win32';
    
    // En Windows el ejecutable es .exe, en Linux no tiene extensión
    const executableName = isWindows ? 'sisfac-backend.exe' : 'sisfac-backend';
    backendExecutable = path.join(resourcesPath, 'backend', executableName);
    projectRoot = resourcesPath;
    
    // Verificar que el ejecutable existe
    if (!fs.existsSync(backendExecutable)) {
      dialog.showErrorBox('Error Crítico', 
        `No se encontró el ejecutable del backend.\n\n` +
        `Buscado en: ${backendExecutable}\n\n` +
        `La aplicación está corrupta o incompleta.\n` +
        `Por favor, reinstale la aplicación.`
      );
      app.quit();
      return;
    }
    
    // En Linux, los permisos se establecen en postinst.sh durante la instalación
    // En Windows no es necesario
  } else {
    // Modo desarrollo: usar Python del venv
    projectRoot = path.join(__dirname, '..');
    const backendScript = path.join(projectRoot, 'backend', 'run.py');
    // Detectar sistema operativo para usar la ruta correcta del venv
    const isWindows = process.platform === 'win32';
    const venvPython = isWindows 
      ? path.join(projectRoot, 'venv', 'Scripts', 'python.exe')
      : path.join(projectRoot, 'venv', 'bin', 'python');
    const pythonCmd = fs.existsSync(venvPython) ? venvPython : (isWindows ? 'python' : 'python3');
    
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
        FLASK_DEBUG: '1',
        SISFAC_PORT: String(port)
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
      SISFAC_PORT: String(port),
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
  const iconPath = getAppIconPath();
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: iconPath,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // Cargar la app Flask
  mainWindow.loadURL(`http://127.0.0.1:${backendPort}/`);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) {
        mainWindow.restore();
      }
      mainWindow.focus();
    } else {
      createWindow();
    }
  });

  app.whenReady().then(async () => {
    backendPort = await getAvailablePort();
    startBackend(backendPort);

    // Esperar a que arranque Flask y luego abrir la ventana
    // Intentar conectar hasta 10 veces (10 segundos máximo)
    let attempts = 0;
    const maxAttempts = 10;
    
    const tryConnect = () => {
      const req = http.get(`http://127.0.0.1:${backendPort}/`, (res) => {
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
}

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

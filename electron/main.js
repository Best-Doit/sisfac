const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

// Deshabilitar sandbox para evitar problemas de permisos en desarrollo
// IMPORTANTE: Debe ejecutarse antes de que app esté listo
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('--disable-setuid-sandbox');

let mainWindow = null;
let backendProcess = null;

function startBackend() {
  const fs = require('fs');
  
  // Detectar si estamos en modo desarrollo o empaquetado
  const isPackaged = app.isPackaged;
  
  let backendExecutable, projectRoot;
  
  if (isPackaged) {
    // Modo empaquetado: usar el ejecutable de PyInstaller
    // El ejecutable está en extraResources/backend/dist/
    const resourcesPath = process.resourcesPath;
    const executableName = process.platform === 'win32' ? 'sisfac-backend.exe' : 'sisfac-backend';
    backendExecutable = path.join(resourcesPath, 'backend', 'dist', executableName);
    projectRoot = resourcesPath;
    
    // Verificar que el ejecutable existe
    if (!fs.existsSync(backendExecutable)) {
      dialog.showErrorBox('Error', 
        `No se encontró el ejecutable del backend.\n\n` +
        `Buscado en: ${backendExecutable}\n\n` +
        `Por favor, verifica la instalación.`
      );
      app.quit();
      return;
    }
  } else {
    // Modo desarrollo: usar Python del venv
    projectRoot = path.join(__dirname, '..');
    const backendScript = path.join(projectRoot, 'backend', 'run.py');
    const venvPython = path.join(projectRoot, 'venv', 'bin', 'python');
    const pythonCmd = process.platform === 'win32'
      ? 'python'
      : (fs.existsSync(venvPython) ? venvPython : 'python3');
    
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
    });
    
    return;
  }

  // Ejecutar el backend empaquetado (sin argumentos, es un ejecutable)
  backendProcess = spawn(backendExecutable, [], {
    cwd: projectRoot,
    env: {
      ...process.env,
      FLASK_ENV: 'production',
      FLASK_DEBUG: '0'
    },
    stdio: 'inherit'
  });

  backendProcess.on('error', (err) => {
    dialog.showErrorBox('Error iniciando backend', 
      `No se pudo iniciar el servidor Flask.\n\n` +
      `Error: ${err.message}\n\n` +
      `Ejecutable: ${backendExecutable}`
    );
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      contextIsolation: true
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

  // Esperar un poco a que arranque Flask y luego abrir la ventana
  setTimeout(createWindow, 1500);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
    backendProcess = null;
  }
});

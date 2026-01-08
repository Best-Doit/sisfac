/**
 * Preload script para Electron
 * Expone APIs seguras al renderer process
 */
const { contextBridge } = require('electron');

// Exponer APIs seguras al renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Aquí puedes agregar APIs específicas si las necesitas en el futuro
  platform: process.platform,
  version: process.versions.electron
});


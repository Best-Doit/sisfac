const fs = require('fs');
const path = require('path');

exports.default = async function(context) {
  const { appOutDir, platform, platformName } = context;
  
  console.log('🔧 Ejecutando afterPack hook...');
  console.log(`   Plataforma: ${platformName || platform || 'desconocida'}`);
  console.log(`   Directorio de salida: ${appOutDir}`);
  
  // Detectar plataforma - puede venir como platform o platformName
  const isLinux = platform === 'linux' || platformName === 'linux';
  
  // Solo procesar para Linux
  if (!isLinux) {
    console.log('   Saltando afterPack para plataforma no-Linux');
    return;
  }
  
  // Verificar que el backend compilado existe
  const backendExecutable = path.join(appOutDir, 'resources', 'backend', 'sisfac-backend');
  
  if (!fs.existsSync(backendExecutable)) {
    console.error(`❌ ERROR CRÍTICO: No se encontró el ejecutable del backend en: ${backendExecutable}`);
    console.error('   El build fallará. Asegúrate de que:');
    console.error('   1. El backend esté compilado con PyInstaller');
    console.error('   2. El ejecutable esté en: backend/dist/sisfac-backend');
    console.error('   3. El package.json tenga la ruta correcta en extraResources');
    throw new Error(`Backend executable not found: ${backendExecutable}`);
  } else {
    // Verificar que el backend existe (los permisos se establecerán en postinst.sh como root)
    console.log('✅ Backend encontrado (permisos se establecerán en postinst.sh)');
  }
  
  // Eliminar el binario chrome-sandbox para evitar problemas de SUID sandbox
  // Esto es necesario para paquetes DEB instalables
  const chromeSandboxPath = path.join(appOutDir, 'chrome-sandbox');
  if (fs.existsSync(chromeSandboxPath)) {
    try {
      fs.unlinkSync(chromeSandboxPath);
      console.log('✅ Eliminado chrome-sandbox para deshabilitar SUID sandbox.');
    } catch (err) {
      console.warn(`⚠️  No se pudo eliminar chrome-sandbox: ${err.message}`);
    }
  }
  
  // Crear wrapper script que se ejecutará en lugar del binario directo
  const wrapperScript = path.join(appOutDir, 'sisfac-wrapper.sh');
  const executablePath = path.join(appOutDir, 'sisfac-desktop');
  const wrapperContent = `#!/bin/bash
# Wrapper script para SISFAC Desktop
# Asegura que las flags de sandbox se apliquen correctamente

export ELECTRON_DISABLE_SANDBOX=1

# Ruta del ejecutable (se establece durante el build)
EXECUTABLE="${executablePath}"

# Si no encontramos el ejecutable en la ruta esperada, usar la ruta de instalación
if [ ! -f "$EXECUTABLE" ]; then
    EXECUTABLE="/opt/SISFAC/sisfac-desktop"
fi

# Ejecutar el ejecutable con flags de sandbox deshabilitadas
exec "$EXECUTABLE" --no-sandbox --disable-setuid-sandbox --disable-zygote "$@"
`;
  
  try {
    fs.writeFileSync(wrapperScript, wrapperContent, { mode: 0o755 });
    fs.chmodSync(wrapperScript, 0o755);
    console.log('✅ Script wrapper creado con flags de sandbox');
  } catch (err) {
    console.warn(`⚠️  No se pudo crear el script wrapper: ${err.message}`);
  }

  // El archivo .desktop se actualizará después de la instalación mediante postinst.sh
  // Aquí solo nos aseguramos de que el icono esté configurado correctamente
  try {
    const productName = context.packager?.appInfo?.productFilename || 'SISFAC';
    const desktopFile = path.join(appOutDir, '..', `${productName}.desktop`);
    if (fs.existsSync(desktopFile)) {
      let desktopContent = fs.readFileSync(desktopFile, 'utf8');
      
      // Asegurar que el icono esté configurado correctamente
      if (!desktopContent.includes('Icon=')) {
        desktopContent += '\nIcon=sisfac-desktop\n';
      } else {
        desktopContent = desktopContent.replace(/Icon=.*/g, 'Icon=sisfac-desktop');
      }
      
      fs.writeFileSync(desktopFile, desktopContent);
      console.log('✅ Archivo .desktop preparado (flags de sandbox se aplicarán en postinst)');
    }
  } catch (err) {
    console.warn(`⚠️  No se pudo actualizar el archivo .desktop: ${err.message}`);
  }
  
  console.log('✅ afterPack completado');
};

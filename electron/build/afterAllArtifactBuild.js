const fs = require('fs');
const path = require('path');

exports.default = async function(context) {
  const { artifactPaths, platformName } = context;
  
  console.log('🔧 Ejecutando afterAllArtifactBuild hook...');
  console.log(`   Plataforma: ${platformName || 'desconocida'}`);
  
  // Buscar el paquete DEB generado
  const debPath = artifactPaths.find(p => p.endsWith('.deb'));
  
  if (debPath && fs.existsSync(debPath)) {
    console.log(`   Paquete DEB encontrado: ${debPath}`);
    console.log('✅ Paquete DEB generado correctamente');
    console.log('ℹ️  chrome-sandbox eliminado en afterPack.js');
    console.log('ℹ️  Los flags de sandbox están configurados en main.js');
    console.log('ℹ️  El archivo .desktop se actualizará automáticamente durante la instalación (postinst.sh)');
    console.log('   El paquete está listo para instalar en Kubuntu/Ubuntu');
  } else {
    console.log('ℹ️  No se encontró paquete DEB (puede ser normal si se generó otro formato)');
  }
  
  console.log('✅ afterAllArtifactBuild completado');
};

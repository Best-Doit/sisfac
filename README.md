# SISFAC - Sistema de Facturación

SISFAC es un sistema de facturación de escritorio (interfaz web embebida) pensado para pequeños negocios.  
La interfaz está construida con Flask (templates Jinja2), Tailwind CSS y Alpine.js; el empaquetado final a escritorio se realiza con Electron (según documentación técnica en `documentacion/`).

## 🚀 Características

- ✅ Gestión completa de clientes (nombre y cédula de identidad)
- ✅ Control de inventario con alertas de stock bajo
- ✅ Sistema de facturación simplificado (sin estados, sin IVA)
- ✅ Múltiples precios por producto (Principal, P1, P2)
- ✅ Historial detallado de facturas por cliente
- ✅ Dashboard con métricas básicas
- ✅ Sistema de backups y restauración
- ✅ Importación masiva desde Excel
- ✅ Búsqueda predictiva en clientes y facturas
- ✅ Interfaz moderna con Tailwind CSS y Alpine.js
- ✅ Sidebar colapsable con estado persistente
- ✅ Diseño responsive listo para integrarse en app de escritorio

## 📋 Requisitos

- Python 3.9+ (recomendado: 3.12)
- Node.js y npm (para empaquetado con Electron)

## 🔧 Instalación

### 🐧 Linux/macOS

**Iniciar la aplicación:**
```bash
./start.sh
```

**Empaquetar (Backend + Electron):**
```bash
./empaquetar.sh
```

### 🪟 Windows

**Preparar entorno:**
```cmd
scripts\preparar_entorno_windows.bat
```

**Iniciar aplicación:**
```cmd
venv\Scripts\activate
cd backend
python run.py
```

**Empaquetar (Backend + Electron):**
```cmd
scripts\empaquetar_windows.bat
```

**Nota:** Si `python` no funciona, usa `py` o `py -3.12`. Si `pip` no funciona, usa `python -m pip`.

## 📁 Estructura del Proyecto

```
SISFAC/
├── backend/
│   ├── app/
│   │   ├── __init__.py        # create_app y configuración Flask/SQLAlchemy
│   │   ├── models.py          # Modelos de base de datos (Cliente, Producto, Factura, DetalleFactura, Talonario)
│   │   ├── routes/            # Rutas de la aplicación (módulos por dominio)
│   │   │   ├── main.py        # Dashboard principal
│   │   │   ├── clientes.py    # CRUD de clientes e historial
│   │   │   ├── inventario.py  # CRUD de productos, stock e importación desde Excel
│   │   │   ├── facturas.py    # Creación/listado de facturas y API de productos
│   │   │   ├── talonarios.py  # Gestión de talonarios y numeración
│   │   │   └── ajustes.py     # Sistema de backups, restaurar y borrar datos
│   │   └── templates/         # Templates HTML (Jinja2 + Tailwind + Alpine.js)
│   │       ├── base.html      # Layout principal, sidebar y sistema global de notificaciones
│   │       ├── index.html     # Dashboard con estadísticas y accesos rápidos
│   │       ├── clientes/      # Vistas de clientes
│   │       ├── inventario/    # Vistas de inventario (lista, formulario, importar Excel)
│   │       ├── facturas/      # Vistas de facturas (flujo guiado "Facturar")
│   │       └── ajustes/      # Vistas de ajustes (backups, restaurar, borrar datos)
│   └── run.py                 # Punto de entrada Flask para desarrollo
├── documentacion/             # Documentación funcional y técnica del sistema
│   ├── README.md              # Índice de documentación
│   ├── ARQUITECTURA_TECNICA.md# Arquitectura técnica (incluye capa Electron)
│   ├── DISENO_API.md          # Diseño de APIs REST (para futuras integraciones)
│   ├── CAMBIOS_RECIENTES.md   # Historial de cambios y mejoras
│   └── guia_desarrollo/       # Guías de desarrollo (backend, frontend, flujos)
├── sisfac.db                  # Base de datos SQLite (se crea automáticamente)
├── backups/                   # Directorio de backups automáticos
├── scripts/                   # Scripts de utilidad
│   ├── preparar_entorno_windows.bat  # Preparar entorno en Windows
│   └── empaquetar_windows.bat        # Empaquetar aplicación en Windows
├── requirements.txt           # Dependencias Python
└── README.md                  # Este archivo
```

## 🎯 Uso Rápido (Flujo funcional)

1. **Dashboard**  
   - Al iniciar, se muestra un panel con métricas: total de clientes, productos, facturas, facturas pendientes y productos con stock bajo.

2. **Clientes**  
   - Alta, edición y baja lógica de clientes (`Clientes` en el menú lateral).  
   - Campos: Nombre y Cédula de Identidad únicamente.
   - Búsqueda predictiva por nombre o CI.  
   - Desde cada cliente puede consultarse su historial completo de facturas.

3. **Inventario**  
   - Alta, edición y baja lógica de productos (`Inventario`).  
   - Campos clave: código único, nombre, 3 precios (principal, P1, P2), stock.  
   - Búsqueda por nombre/código.  
   - Importación masiva desde Excel (`Inventario` → `Importar Excel`), con plantilla descargable.
   - Validación: No se permite agregar productos con stock 0 al carrito de facturación.

4. **Facturación**  
   - Flujo guiado: `Facturar` en el menú → selección de productos (carrito), datos de cliente y emisión.  
   - Campos: Número de factura, talonario, cliente, fecha de emisión.  
   - Selección de precio por producto (Principal, P1, P2) con botón desplegable azul.
   - Tabla de factura ocupa toda la pantalla con scroll automático.
   - Actualización automática de stock al facturar.
   - Validación de stock: No permite exceder stock disponible.

5. **Historial de Facturas**  
   - Listado completo de facturas con filtros por número y rango de fechas.  
   - Búsqueda predictiva por número de factura.
   - Desde el listado se puede acceder al detalle de cada factura.
   - Sin estados: El sistema funciona como respaldo virtual de facturas físicas.

6. **Talonarios**  
   - Gestión de talonarios (rango numérico y prefijo) y activación/desactivación.  
   - Cada talonario define un rango de números utilizables para facturación.

7. **Ajustes**  
   - Crear backup: Genera copias de seguridad automáticas con timestamp.
   - Restaurar backup: Permite restaurar desde archivo .db.
   - Lista de backups: Muestra todos los backups disponibles.
   - Borrar datos: Elimina todos los datos con confirmación doble (crea backup automático).

## 📝 Notas

- La base de datos SQLite se crea automáticamente al iniciar
- Los datos se guardan en `sisfac.db` en la raíz del proyecto
- El sistema calcula automáticamente totales (sin IVA)
- El stock se actualiza automáticamente al facturar
- Los backups se guardan en el directorio `backups/`
- El sidebar colapsable mantiene su estado durante la navegación


## 🔮 Próximas Mejoras

- Exportación a PDF de facturas
- Exportación a Excel de reportes
- Dashboard con gráficos
- Búsqueda avanzada con múltiples filtros

## 📄 Licencia

Este proyecto está bajo una licencia de **uso no comercial**. 

**Permisos:**
- ✅ Ver y estudiar el código
- ✅ Usar el software para fines personales o educativos
- ✅ Modificar el código para uso personal
- ✅ Compartir el código con atribución

**Restricciones:**
- ❌ No se permite uso comercial sin autorización
- ❌ No se permite redistribución comercial
- ❌ No se permite modificación para uso comercial sin permiso

Para uso comercial, contactar al autor.

---

## 👤 Créditos y Autor

**Desarrollado por:** Best_Doit

**Redes Sociales:**
- 🎵 TikTok: [@best_doit](https://www.tiktok.com/@best_doit)

---

## 📚 Documentación

Para documentación completa del sistema, consulta:
- [Documentación Técnica](./documentacion/README.md) - Índice completo de documentación
- [Cambios Recientes](./documentacion/CAMBIOS_RECIENTES.md) - Historial de mejoras
- [Arquitectura Técnica](./documentacion/ARQUITECTURA_TECNICA.md) - Detalles técnicos
- [Guía de Desarrollo](./documentacion/guia_desarrollo/README.md) - Guías para desarrolladores

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## ⚠️ Disclaimer

Este software se proporciona "tal cual", sin garantías de ningún tipo. El autor no se hace responsable de cualquier daño derivado del uso de este software.

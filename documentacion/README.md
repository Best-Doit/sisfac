# Documentación del Sistema SISFAC

Bienvenido a la documentación completa del Sistema de Facturación (SISFAC).

## 📚 Índice de Documentos

### 1. [Arquitectura Técnica](./ARQUITECTURA_TECNICA.md)
**Documento de Arquitectura del Sistema**

Detalles técnicos de la arquitectura:
- Arquitectura de alto nivel
- Arquitectura de capas (Presentación, Aplicación, Datos)
- Flujo de datos
- Comunicación entre componentes
- Gestión de estado
- Manejo de errores
- Seguridad
- Rendimiento y optimización
- Escalabilidad

**👨‍💻 Para desarrolladores:** Documento esencial para entender la estructura técnica.

---

### 2. [Diseño de API](./DISENO_API.md)
**Especificación de APIs REST**

Documentación completa de la API:
- Convenciones de API
- Formato de respuestas
- Manejo de errores
- Endpoints de Clientes
- Endpoints de Productos
- Endpoints de Facturas
- Endpoints de Dashboard
- Ejemplos de uso en JavaScript

**🔌 Para integración:** Documento necesario para consumir las APIs.

---

## 🎯 Stack Tecnológico

### Frontend
- **Tailwind CSS 3.x**: Framework de utilidades CSS
- **Alpine.js 3.x**: Framework JavaScript ligero
- **HTML5**: Estructura semántica
- **Electron**: Empaquetado para escritorio

### Backend
- **Flask 2.x**: Framework web (Server-Side Rendering)
- **FastAPI**: Framework para APIs REST
- **SQLAlchemy 2.x**: ORM
- **SQLite**: Base de datos

### Utilidades
- **ReportLab/WeasyPrint**: Generación de PDFs
- **openpyxl**: Exportación a Excel
- **python-dateutil**: Manejo de fechas

---

## 📋 Módulos del Sistema

### 1. Módulo de Clientes
- CRUD completo de clientes (nombre y CI únicamente)
- Búsqueda predictiva
- Vista detallada con historial completo de facturas

### 2. Módulo de Inventario
- CRUD completo de productos
- Control de stock en tiempo real
- Alertas de stock bajo
- Múltiples precios (Principal, P1, P2)
- Importación masiva desde Excel
- Plantilla descargable para importación

### 3. Módulo de Facturación
- Creación de facturas con flujo guiado
- Múltiples productos por factura
- Cálculo automático de totales (sin IVA)
- Selección de precios (Principal, P1, P2)
- Validación de stock en tiempo real
- Tabla de factura optimizada para pantalla completa

### 4. Módulo de Historial
- Listado completo de facturas
- Búsqueda predictiva por número de factura
- Filtros por fecha
- Vista detallada de cada factura
- Historial por cliente

### 5. Dashboard
- Estadísticas generales
- Resumen de ventas
- Productos con stock bajo

### 6. Módulo de Ajustes
- Crear backups automáticos
- Restaurar backups
- Lista y descarga de backups
- Borrar todos los datos (con backup automático)

---

## 🚀 Inicio Rápido

### Para Desarrolladores

1. **Revisar Arquitectura**: Entender estructura técnica
2. **Consultar API**: Conocer endpoints disponibles
3. **Leer Guías de Desarrollo**: Backend, frontend y flujos funcionales
4. **Revisar Cambios Recientes**: Conocer las últimas mejoras

### Para Usuarios

1. **Leer README Principal**: Instalación y uso básico
2. **Consultar Guía de Flujos**: Entender cómo usar cada funcionalidad
3. **Revisar Cambios Recientes**: Conocer nuevas características

---

## 📝 Convenciones de Documentación

- **RF-XXX**: Requisitos Funcionales
- **RNF-XXX**: Requisitos No Funcionales
- **CU-XXX**: Casos de Uso
- **GET/POST/PUT/DELETE**: Métodos HTTP
- **200/400/404/500**: Códigos de estado HTTP

---

## 🔄 Versión de Documentación

- **Versión Actual**: 1.3
- **Fecha**: Enero 2025
- **Estado**: En Desarrollo Activo

---

## 📝 Cambios Recientes

### [Cambios Recientes y Mejoras](./CAMBIOS_RECIENTES.md)
**Documento de Actualizaciones**

Este documento describe los cambios, mejoras y nuevas funcionalidades implementadas recientemente:
- ✅ Funcionalidad de anulación de facturas con reversión de stock
- ✅ Mejoras en la tabla de facturación (controles de cantidad con botones +/-, dropdown de precios mejorado)
- ✅ Optimizaciones de layout (sin scroll en pantalla principal, tabla ocupa todo el espacio)
- ✅ Importación de clientes desde Excel con plantilla descargable
- ✅ Sistema de precios unificado (solo P1 y P2, con P1 como principal y más alto)
- ✅ Búsqueda predictiva automática sin ventanas emergentes (filtrado directo en tablas)
- ✅ Mejora en numeración de facturas (n+1 con sugerencia sin incrementar)
- ✅ Botón de TikTok en sidebar
- ✅ Correcciones de UI/UX (footer, tabla de inventario simplificada)

**📖 Leer para estar al día:** Este documento para conocer las últimas mejoras del sistema.

---

## 📞 Contacto

Para preguntas sobre la documentación o el proyecto, contactar al equipo de desarrollo.

---

**Última actualización**: 2024


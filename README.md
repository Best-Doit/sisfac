# SISFAC

Sistema de facturacion para escritorio orientado a pequenos negocios.

SISFAC permite:
- registrar clientes
- administrar inventario
- emitir facturas con numeracion por talonario
- exportar e importar datos por Excel
- crear y restaurar backups

## Descarga

Los instaladores oficiales se publican en GitHub Releases:

https://github.com/Best-Doit/sisfac/releases

## Uso Rapido

### Windows

1. Descarga el instalador desde `Releases`.
2. Instala SISFAC.
3. Abre la aplicacion desde el acceso directo.

Si estas usando el proyecto en modo desarrollo:

```powershell
.\start.ps1
```

O en CMD:

```cmd
start.bat
```

### Linux

Para desarrollo:

```bash
./start.sh
```

Para empaquetar:

```bash
./empaquetar.sh
```

## Lo Mas Importante

- `P1` es el precio de venta mas alto.
- `P2` es un precio alternativo mas bajo.
- La numeracion de facturas puede manejarse por talonario.
- El sistema puede exportar e importar datos por Excel.
- Antes de operaciones delicadas, usa backups.

## Requisitos Para Desarrollo

- Python 3.9 o superior
- Node.js y npm

## Estructura

```text
SISFAC/
|-- backend/
|-- electron/
|-- documentacion/
|-- requirements.txt
|-- start.bat
|-- start.ps1
|-- start.sh
```

## Documentacion

La documentacion tecnica esta en [documentacion/README.md](./documentacion/README.md).

Archivos utiles:
- [documentacion/CHANGELOG.md](./documentacion/CHANGELOG.md)
- [documentacion/EMPAQUETADO.md](./documentacion/EMPAQUETADO.md)
- [documentacion/ARQUITECTURA_TECNICA.md](./documentacion/ARQUITECTURA_TECNICA.md)

## Licencia

Uso no comercial.

## Creditos

Desarrollado por Best_Doit.

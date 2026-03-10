; NSIS include file for SISFAC installer
; Personalización del instalador / desinstalador.

; -------------------------------------------------------------------
; El backend empaquetado guarda los datos de usuario en:
;   %USERPROFILE%\.sisfac
; Allí viven:
;   - sisfac.db        (base de datos)
;   - backups\*.db     (backups automáticos)
;   - uploads\*        (archivos temporales/subidos)
; -------------------------------------------------------------------

!macro customUnInstall
  ; El usuario ha decidido desinstalar SISFAC.
  ; Además de la carpeta de instalación, limpiamos la carpeta de datos.

  ; Borrar completamente la carpeta de datos del usuario: C:\Users\<User>\.sisfac
  ; (si no existe, este comando no genera error).
  RMDir /r "$PROFILE\.sisfac"
!macroend

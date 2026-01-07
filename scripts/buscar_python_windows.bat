@echo off
REM Script auxiliar para buscar Python en Windows
REM Establece PYTHON_CMD y PYTHON_FOUND si encuentra Python

SETLOCAL ENABLEDELAYEDEXPANSION

SET PYTHON_CMD=
SET PYTHON_FOUND=0

REM Método 1: python directo
python --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=python
    SET PYTHON_FOUND=1
    ENDLOCAL & SET PYTHON_CMD=python & SET PYTHON_FOUND=1
    EXIT /B 0
)

REM Método 2: py launcher (múltiples variantes)
py --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py
    SET PYTHON_FOUND=1
    ENDLOCAL & SET PYTHON_CMD=py & SET PYTHON_FOUND=1
    EXIT /B 0
)

py -3 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3
    SET PYTHON_FOUND=1
    ENDLOCAL & SET PYTHON_CMD=py -3 & SET PYTHON_FOUND=1
    EXIT /B 0
)

py -3.12 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.12
    SET PYTHON_FOUND=1
    ENDLOCAL & SET PYTHON_CMD=py -3.12 & SET PYTHON_FOUND=1
    EXIT /B 0
)

py -3.11 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.11
    SET PYTHON_FOUND=1
    ENDLOCAL & SET PYTHON_CMD=py -3.11 & SET PYTHON_FOUND=1
    EXIT /B 0
)

py -3.10 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.10
    SET PYTHON_FOUND=1
    ENDLOCAL & SET PYTHON_CMD=py -3.10 & SET PYTHON_FOUND=1
    EXIT /B 0
)

py -3.9 --version >nul 2>&1
IF NOT ERRORLEVEL 1 (
    SET PYTHON_CMD=py -3.9
    SET PYTHON_FOUND=1
    ENDLOCAL & SET PYTHON_CMD=py -3.9 & SET PYTHON_FOUND=1
    EXIT /B 0
)

REM Método 3: Buscar en ubicaciones comunes
IF EXIST "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python39\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "%ProgramFiles%\Python312\python.exe" (
    "%ProgramFiles%\Python312\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python312\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%ProgramFiles%\Python312\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "%ProgramFiles%\Python311\python.exe" (
    "%ProgramFiles%\Python311\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python311\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%ProgramFiles%\Python311\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "%ProgramFiles%\Python310\python.exe" (
    "%ProgramFiles%\Python310\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python310\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%ProgramFiles%\Python310\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "%ProgramFiles%\Python39\python.exe" (
    "%ProgramFiles%\Python39\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="%ProgramFiles%\Python39\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="%ProgramFiles%\Python39\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "C:\Python312\python.exe" (
    "C:\Python312\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python312\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="C:\Python312\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "C:\Python311\python.exe" (
    "C:\Python311\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python311\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="C:\Python311\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "C:\Python310\python.exe" (
    "C:\Python310\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python310\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="C:\Python310\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

IF EXIST "C:\Python39\python.exe" (
    "C:\Python39\python.exe" --version >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        SET PYTHON_CMD="C:\Python39\python.exe"
        SET PYTHON_FOUND=1
        ENDLOCAL & SET PYTHON_CMD="C:\Python39\python.exe" & SET PYTHON_FOUND=1
        EXIT /B 0
    )
)

REM No se encontró Python
ENDLOCAL & SET PYTHON_CMD= & SET PYTHON_FOUND=0
EXIT /B 1





@echo off
setlocal

:menu
cls
echo.
echo 1. Ejecutar script 1
echo 2. Ejecutar script 2
echo 3. Salir
echo.
set /p opcion="Introduce una opción: "

if "%opcion%"=="1" (
    call :script1
    goto :menu
)
if "%opcion%"=="2" (
    call :script2
    goto :menu
)
if "%opcion%"=="3" (
    exit /b
)
goto :menu

:script1
echo Ejecutando script 1...
REM Aquí puedes poner los comandos para tu script 1.
REM Por ejemplo, para almacenar la dirección IP pública en un archivo:
curl ifconfig.me > "Public IP.txt"
goto :eof

:script2
echo Ejecutando script 2...
REM Aquí puedes poner los comandos para tu script 2.
goto :eof

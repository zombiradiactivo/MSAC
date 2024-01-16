@echo off
:: Comprueba si el script se está ejecutando como administrador y, si no, lo reinicia como administrador
openfiles >nul 2>&1 
if %errorlevel% equ 0 ( 
    echo Ejecutando como administrador
) else (
    echo No se está ejecutando como administrador. Reiniciando como administrador...
    Powershell -Command "Start-Process -Verb RunAs '%0'"
    exit /b
)

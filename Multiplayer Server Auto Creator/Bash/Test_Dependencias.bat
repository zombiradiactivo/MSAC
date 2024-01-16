@echo off
cls
goto :menu
goto :eof

:menu
cls
echo.
echo ::::    ::::   ::::::::      :::      ::::::::  
echo +:+:+: :+:+:+ :+:    :+:   :+: :+:   :+:    :+: 
echo +:+ +:+:+ +:+ +:+         +:+   +:+  +:+        
echo +#+  +:+  +#+ +#++:++#++ +#++:++#++: +#+        
echo +#+       +#+        +#+ +#+     +#+ +#+        
echo #+#       #+# #+#    #+# #+#     #+# #+#    #+# 
echo ###       ###  ########  ###     ###  ########   
echo.
echo.
echo		Escoge una opcion
echo.   
echo 1. Guia para instalar manualmente Chocolatey
echo 2. Apache (Necesita Chocolatey)
echo 0. Salir
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    goto :Install_Choco
)
if "%opcion%"=="2" (
    goto :Apache
)
if "%opcion%"=="0" (
    exit /b
)

goto :eof

:Install_Choco
REM Guia para instalar Chocolatey 
REM Comprobar si Chocolatey está instalado
where /q choco
if %ERRORLEVEL% neq 0 (
    echo Instalando Chocolatey...
	start "" "https://community.chocolatey.org/courses/installation/installing?method=installing-chocolatey#cmd"
	pause
	cls
	goto :menu
	goto :eof
)
echo Ya esta instalado

goto :menu
goto :eof

:Apache
# REM Instalar Apache
echo Instalando Apache...
where /q choco
if %ERRORLEVEL% neq 0 (
	echo  Chocolatey no esta intalado
	pause
	cls
	goto :menu
	goto :eof
)
choco install apache-httpd
pause
cls
goto :menu
goto :eof

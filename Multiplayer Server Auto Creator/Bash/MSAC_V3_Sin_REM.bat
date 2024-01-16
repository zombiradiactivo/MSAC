@echo off
setlocal


curl ifconfig.me > "Public IP.txt"
mkdir servers
goto :menu
goto :eof

:menu
cls
Color 09
echo.
echo ::::    ::::   ::::::::      :::      ::::::::  
echo +:+:+: :+:+:+ :+:    :+:   :+: :+:   :+:    :+: 
echo +:+ +:+:+ +:+ +:+         +:+   +:+  +:+        
echo +#+  +:+  +#+ +#++:++#++ +#++:++#++: +#+        
echo +#+       +#+        +#+ +#+     +#+ +#+        
echo #+#       #+# #+#    #+# #+#     #+# #+#    #+# 
echo ###       ###  ########  ###     ###  ########   
echo.
echo 		Escoge una opcion
echo 1. Server 
echo 2. Juegos 
echo 0. Salir
echo.
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    goto :Menu_Servers
)
if "%opcion%"=="2" (
    goto :Menu_Games
)
if "%opcion%"=="0" (
    exit /b
)

:Menu_Servers
cls
Color 0a
echo.
echo  ::::::::  :::::::::: :::::::::  :::     ::: :::::::::: :::::::::   ::::::::  
echo :+:    :+: :+:        :+:    :+: :+:     :+: :+:        :+:    :+: :+:    :+: 
echo +:+        +:+        +:+    +:+ +:+     +:+ +:+        +:+    +:+ +:+        
echo +#++:++#++ +#++:++#   +#++:++#:  +#+     +:+ +#++:++#   +#++:++#:  +#++:++#++ 
echo        +#+ +#+        +#+    +#+  +#+   +#+  +#+        +#+    +#+        +#+ 
echo #+#    #+# #+#        #+#    #+#   #+#+#+#   #+#        #+#    #+# #+#    #+# 
echo  ########  ########## ###    ###     ###     ########## ###    ###  ########  
echo.
echo.
echo		Escoge una opcion
echo.   
echo 1. Chocolatey (Guia para instalar manualmente)
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
    goto :menu
)

goto :eof

:Install_Choco
where /q choco
if %ERRORLEVEL% neq 0 (
    echo Instalando Chocolatey...
	start "" "https://community.chocolatey.org/courses/installation/installing?method=installing-chocolatey#cmd"
	pause
	cls
	goto :Menu_Servers
	goto :eof
)
echo Ya esta instalado

goto :Menu_Servers
goto :eof

:Apache
echo Instalando Apache...
where /q choco
if %ERRORLEVEL% neq 0 (
	echo  Chocolatey no esta intalado
	pause
	cls
	goto :Menu_Servers
	goto :eof
)
choco install apache-httpd
pause
cls
goto :Menu_Servers
goto :eof


:Menu_Games
cls
Color 0b
echo.
echo  ::::::::      :::     ::::    ::::  :::::::::: ::::::::  
echo :+:    :+:   :+: :+:   +:+:+: :+:+:+ :+:       :+:    :+: 
echo +:+         +:+   +:+  +:+ +:+:+ +:+ +:+       +:+        
echo :#:        +#++:++#++: +#+  +:+  +#+ +#++:++#  +#++:++#++ 
echo +#+   +#+# +#+     +#+ +#+       +#+ +#+              +#+ 
echo #+#    #+# #+#     #+# #+#       #+# #+#       #+#    #+# 
echo  ########  ###     ### ###       ### ########## ########  
echo.
echo 		Escoge una opcion
echo 1. Minecraft
echo 2. Satisfactory
echo 3. Starbound
echo 9. Create Content Folder (Necesario para Minecraft)
echo 0. Salir
echo.
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    goto :Minecraft_Menu
)
if "%opcion%"=="2" (
    goto :Satisfactory_Menu
)
if "%opcion%"=="3" (
    goto :Starbound_Menu
)
if "%opcion%"=="9" (
    call :Content_Folder
)
if "%opcion%"=="0" (
    goto :menu
)
goto :Menu_Games

:Content_Folder

echo Content Folder
set carpeta="content"
if exist "%carpeta%\" (
    echo La carpeta %carpeta% existe.
    echo Ya esta creado.
	pause
	goto :Menu_Games
) else (
    echo La carpeta %carpeta% no existe.
	echo Creando
	mkdir content
	mkdir content\MC
	mkdir content\MCF
	echo eula=true > "content\MC\eula.txt"
	echo eula=true > "content\MCF\eula.txt"

	goto :Menu_Games
)
goto :Menu_Games
goto :eof

:Minecraft_Menu
cls
echo ---Minecraft Menu---
echo.
echo 1. Vanilla
echo 2. Forge 
echo 3. Add Windows firewall rule "(Se necesita permisos de administrdor)"
echo 0. Volver
echo.
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="2" (
    goto :Minecraft_Menu_Forge
)
if "%opcion%"=="3" (
    call :Minecraft_Firewall
	goto :Minecraft_Menu
)
if "%opcion%"=="0" (
    goto :Menu_Games
)
goto :Minecraft_Menu
goto :eof 


:Minecraft_Firewall
	netsh advfirewall firewall add rule name="Minecraft TCP" dir=in action=allow protocol=TCP localport=25565
	netsh advfirewall firewall add rule name="Minecraft UDP" dir=in action=allow protocol=UDP localport=25565
	
:Minecraft_Menu_Vanilla
cls
echo ---Minecraft Menu---
mkdir servers\MCvanilla
echo.
echo  1. 1.20.2
echo  2. 1.19.4
echo  3. 1.18.2
echo  4. 1.17.1
echo  5. 1.16.5
echo  6. 1.15.2
echo  7. 1.14.4
echo  8. 1.13.2
echo  9. 1.12.2
echo 10. 1.11.2
echo 11. 1.10.2
echo 12. 1.9.4
echo 13. 1.8.9
echo 14. 1.7.10
echo 15. 1.6.4
echo 16. 1.5.2
echo 17. 1.4.7
echo 18. 1.3.2
echo 19. 1.2.5
echo 0. Volver
echo.
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    call :Minecraft_Vanilla_1_20_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="2" (
    call :Minecraft_Vanilla_1_19_4
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="3" (
    call :Minecraft_Vanilla_1_18_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="4" (
    call :Minecraft_Vanilla_1_17_1
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="5" (
    call :Minecraft_Vanilla_1_16_5
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="6" (
    call :Minecraft_Vanilla_1_15_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="7" (
    call :Minecraft_Vanilla_1_14_4
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="8" (
    call :Minecraft_Vanilla_1_13_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="9" (
    call :Minecraft_Vanilla_1_12_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="10" (
    call :Minecraft_Vanilla_1_11_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="11" (
    call :Minecraft_Vanilla_1_10_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="12" (
    call :Minecraft_Vanilla_1_9_4
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="13" (
    call :Minecraft_Vanilla_1_8_9
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="14" (
    call :Minecraft_Vanilla_1_7_10
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="15" (
    call :Minecraft_Vanilla_1_6_4
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="16" (
    call :Minecraft_Vanilla_1_5_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="17" (
    call :Minecraft_Vanilla_1_4_7
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="18" (
    call :Minecraft_Vanilla_1_3_2
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="19" (
    call :Minecraft_Vanilla_1_2_5
	goto :Minecraft_Menu_Vanilla
)
if "%opcion%"=="0" (
    goto :Minecraft_Menu
)
goto :Minecraft_Menu_Vanilla
goto :eof 


:Minecraft_Vanilla_1_20_2

set "version=1.20.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/5b868151bd02b41319f54c8d4061b8cae84e665c/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_19_4

set "version=1.19.4"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_18_2

set "version=1.18.4"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_17_1

set "version=1.17.1"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_16_5

set "version=1.16.5"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_15_2

set "version=1.15.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)

cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_14_4

set "version=1.14.4"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_13_2

set "version=1.13.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/3737db93722a9e39eeada7c27e7aca28b144ffa7/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_12_2

set "version=1.12.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_11_2

set "version=1.11.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/f00c294a1576e03fddcac777c3cf4c7d404c4ba4/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_10_2

set "version=1.10.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/3d501b23df53c548254f5e3f66492d178a48db63/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_9_4

set "version=1.9.4"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/edbb7b1758af33d365bf835eb9d13de005b1e274/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_8_9

set "version=1.8.9"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://launcher.mojang.com/v1/objects/b58b2ceb36e01bcd8dbf49c8fb66c55a9f0676cd/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_7_10

set "version=1.7.10"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://launcher.mojang.com/v1/objects/952438ac4e01b4d115c5fc38f891710c4941df29/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_6_4

set "version=1.6.4"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://launcher.mojang.com/v1/objects/050f93c1f3fe9e2052398f7bd6aca10c63d64a87/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 

echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_5_2

set "version=1.5.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://launcher.mojang.com/v1/objects/f9ae3f651319151ce99a0bfad6b34fa16eb6775f/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_4_7

set "version=1.4.7"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://launcher.mojang.com/v1/objects/2f0ec8efddd2f2c674c77be9ddb370b727dec676/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_3_2

set "version=1.3.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://launcher.mojang.com/v1/objects/3de2ae6c488135596e073a9589842800c9f53bfe/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Vanilla_1_2_5

set "version=1.2.5"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://launcher.mojang.com/v1/objects/d8321edc9470e56b8ad5c67bbd16beba25843336/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)
cd "%serverdir%"
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause
(
echo copiando files
copy "%eulafile%" .
)
pause 
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof


:Minecraft_Menu_Forge
echo Minecraft Menu Forge
mkdir servers\MCForge
echo.
echo  1. 1.20.2
echo  2. 1.19.4
echo  3. 1.18.2
echo  4. 1.17.1
echo  5. 1.16.5
echo  6. 1.15.2
echo  7. 1.14.4
echo  8. 1.13.2
echo  9. 1.12.2
echo 10. 1.11.2
echo 11. 1.10.2
echo 12. 1.9.4
echo 13. 1.8.9
echo 14. 1.7.10
echo 15. 1.6.4
echo 16. 1.5.2
echo 17. 1.4.7
echo 18. 1.3.2
echo 19. 1.2.5
echo 0. Volver
echo.
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    call :Minecraft_Forge_1_20_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="2" (
    call :Minecraft_Forge_1_19_4
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="3" (
    call :Minecraft_Forge_1_18_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="4" (
    call :Minecraft_Forge_1_17_1
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="5" (
    call :Minecraft_Forge_1_16_5
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="6" (
    call :Minecraft_Forge_1_15_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="7" (
    call :Minecraft_Forge_1_14_4
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="8" (
    call :Minecraft_Forge_1_13_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="9" (
    call :Minecraft_Forge_1_12_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="10" (
    call :Minecraft_Forge_1_11_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="11" (
    call :Minecraft_Forge_1_10_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="12" (
    call :Minecraft_Forge_1_9_4
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="13" (
    call :Minecraft_Forge_1_8_9
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="14" (
    call :Minecraft_Forge_1_7_10
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="15" (
    call :Minecraft_Forge_1_6_4
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="16" (
    call :Minecraft_Forge_1_5_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="17" (
    call :Minecraft_Forge_1_4_7
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="18" (
    call :Minecraft_Forge_1_3_2
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="19" (
    call :Minecraft_Forge_1_2_5
	goto :Minecraft_Menu_Forge
)
if "%opcion%"=="0" (
    goto :Minecraft_Menu
)
goto :Minecraft_Menu_Forge
goto :eof 


:Minecraft_Forge_1_20_2

echo Descargando 
mkdir servers\MCForge\1.20.2
cd servers\MCForge\1.20.2

if exist "run.bat" (
    echo El servidor se ejecutara.
	start run.bat
	pause
) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.20.2.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.2-48.0.13/forge-1.20.2-48.0.13-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.20.2.Forge.jar" nogui
	pause
	start run.bat
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.20.2\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.20.2
	start run.bat
	pause
)
cd ..
cd ..
cd ..
goto :eof

:Minecraft_Forge_1_19_4

echo Descargando 
mkdir servers\MCForge\1.19.4
cd servers\MCForge\1.19.4

if exist "run.bat" (
    echo El servidor se ejecutara.
	start run.bat

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.19.4.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.2.2/forge-1.19.4-45.2.2-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.19.4.Forge.jar" nogui
	pause
	start run.bat
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.19.4\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.19.4
	start run.bat
	pause
)
cd ..
cd ..
cd ..
goto :eof


:Minecraft_Forge_1_18_2

echo Descargando 
mkdir servers\MCForge\1.18.2
cd servers\MCForge\1.18.2

if exist "run.bat" (
    echo El servidor se ejecutara.
	start run.bat

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.18.2.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.18.2-40.2.10/forge-1.18.2-40.2.10-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.18.2.Forge.jar" nogui
	pause
	start run.bat
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.18.2\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.18.2
	start run.bat
	pause
)
cd ..
cd ..
cd ..
goto :eof


:Minecraft_Forge_1_17_1

echo Descargando 
mkdir servers\MCForge\1.17.1
cd servers\MCForge\1.17.1

if exist "run.bat" (
    echo El servidor se ejecutara.
	start run.bat

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.17.1.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.17.1-37.1.1/forge-1.17.1-37.1.1-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.17.1.Forge.jar" nogui
	pause
	start run.bat
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.17.1\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.17.1
	start run.bat
	pause
)
cd ..
cd ..
cd ..
goto :eof


:Minecraft_Forge_1_16_5

echo Descargando 
mkdir servers\MCForge\1.16.5
cd servers\MCForge\1.16.5

if exist "minecraft_server.1.16.5.jar" (
    echo El servidor se ejecutara.
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.16.5.jar" nogui

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.16.5.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.5-36.2.39/forge-1.16.5-36.2.39-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.16.5.Forge.jar" nogui
	pause
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.16.5.jar" nogui
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.16.5\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.16.5
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.16.5.jar" nogui
)
cd ..
cd ..
cd ..
goto :eof


:Minecraft_Forge_1_15_2

echo Descargando 
mkdir servers\MCForge\1.15.2
cd servers\MCForge\1.15.2

if exist "minecraft_server.1.15.2.jar" (
    echo El servidor se ejecutara.
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.15.2.jar" nogui

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.15.2.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.15.2-31.2.57/forge-1.15.2-31.2.57-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.15.2.Forge.jar" nogui
	pause
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.15.2.jar" nogui
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.15.2\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.15.2
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.15.2.jar" nogui
)
cd ..
cd ..
cd ..
goto :eof


:Minecraft_Forge_1_14_4

echo Descargando 
mkdir servers\MCForge\1.14.4
cd servers\MCForge\1.14.4

if exist "minecraft_server.1.14.4.jar" (
    echo El servidor se ejecutara.
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.14.4.jar" nogui

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.14.4.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.14.4-28.2.26/forge-1.14.4-28.2.26-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.14.4.Forge.jar" nogui
	pause
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.14.4.jar" nogui
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.14.4\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.14.4
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.14.4.jar" nogui
)
cd ..
cd ..
cd ..
goto :eof


:Minecraft_Forge_1_13_2

echo Descargando 
mkdir servers\MCForge\1.13.2
cd servers\MCForge\1.13.2

if exist "minecraft_server.1.13.2.jar" (
    echo El servidor se ejecutara.
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.13.2.jar" nogui

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.13.2.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.13.2-25.0.223/forge-1.13.2-25.0.223-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.13.2.Forge.jar" nogui
	pause
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.13.2.jar" nogui
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.13.2\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.13.2
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.13.2.jar" nogui
)
cd ..
cd ..
cd ..
goto :eof


:Minecraft_Forge_1_12_2

echo Descargando 
mkdir servers\MCForge\1.12.2
cd servers\MCForge\1.12.2

if exist "minecraft_server.1.12.2.jar" (
    echo El servidor se ejecutara.
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.12.2.jar" nogui

) else (
    echo El archivo no existe y se descargara.
	curl -o "server.1.12.2.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.12.2-14.23.5.2860/forge-1.12.2-14.23.5.2860-installer.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.12.2.Forge.jar" nogui
	pause
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.12.2.jar" nogui
	pause
	cd ..
	cd ..
	cd ..
	copy "content\MCF\eula.txt" "servers\MCForge\1.12.2\eula.txt"
	pause
	cls
	echo El servidor se ejecutara.
	cd servers\MCForge\1.12.2
	java -Xmx2048M -Xms2048M -jar "minecraft_server.1.12.2.jar" nogui
)
cd ..
cd ..
cd ..
goto :eof


----------------------------------------------------------------------------------------------


:Satisfactory_Menu
cls
echo ---Satisfactory Menu--
echo Tienes que tener tener comprado Satisfactory en Steam
echo 1. Install or Run
echo 0. Volver
echo.
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    call :Satisfactory_Install_Run
	goto :Satisfactory_Menu
)
if "%opcion%"=="0" (
    goto :Menu_Games
)
goto :Satisfactory_Menu
goto :eof 



:Satisfactory_Install_Run

set "programa=Satisfactory Dedicated Server"
wmic product where name="%programa%" get name >nul 2>&1
if errorlevel 1 (
    echo El programa %programa% no está instalado.
	start steam://install/1690800
) else (
    echo El programa %programa% está instalado.
	start steam://rungameid/1690800
)
goto :Satisfactory_Menu
goto :eof



---------------------------------------------------------------------------------------

:Starbound_Menu 

cls
echo ---Starbound Menu--
echo Tienes que tener tener comprado Starbound en Steam
echo 1. Install or Run
echo 0. Volver
echo.
set /p opcion="Introduce una opcion: "

if "%opcion%"=="1" (
    call :Starbound_Install_Run
	goto :Starbound_Menu
)
if "%opcion%"=="0" (
    goto :Menu_Games
)
goto :Starbound_Menu
goto :eof 




:Starbound_Install_Run
set "programa=Starbound Dedicated Server"
wmic product where name="%programa%" get name >nul 2>&1
if errorlevel 1 (
    echo El programa %programa% no está instalado.
	start steam://install/533830
) else (
    echo El programa %programa% está instalado.
	start steam://rungameid/533830
)
goto :Starbound_Menu
goto :eof





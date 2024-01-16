@echo off
setlocal
setlocal enabledelayedexpansion


:menu
cd %CD%
cls

echo.
echo 1. Ejecutar script 1
echo 2. Test
echo 3. Create Content Folder (Necesario para Minecraft)
echo 0. Salir
echo.
set /p opcion="Introduce una opción: "

if "%opcion%"=="1" (
    call :script_apache
    goto :menu
)
if "%opcion%"=="2" (
    call :Test
    goto :menu
)
if "%opcion%"=="3" (
   	call :Content_Folder
    goto :menu
)

if "%opcion%"=="0" (
    exit /b
)
goto :menu

:script_apache

set "serverinstallerdir=%CD%\servers\Apache_Installer\"
set "serverinstaller=%CD%\servers\Apache_Installer\xampp-windows-x64-8.2.4-0-VS16-installer.exe"
set "downloadurl=https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/8.2.4/xampp-windows-x64-8.2.4-0-VS16-installer.exe/download#"


REM Crear directorio del servidor si no existe
if not exist "%serverinstallerdir%" (
    mkdir "%serverinstallerdir%"
)

cd "%serverinstallerdir%"

REM Descargar el archivo del servidor si no existe
if not exist "%serverinstaller%" (
    echo Descargando...
    curl -o "%serverinstaller%" "%downloadurl%"
)

REM Ejecuta el fichero de instalacion
"%CD%\servers\Apache_Installer\xampp-windows-x64-8.2.4-0-VS16-installer.exe"


goto :eof

:script1
REM Definir variables
set "version=1.20.2"
set "serverfile=%CD%\servers\MCvanilla\%version%\server.%version%.jar"
set "downloadurl=https://piston-data.mojang.com/v1/objects/5b868151bd02b41319f54c8d4061b8cae84e665c/server.jar"
set "serverdir=%CD%\servers\MCvanilla\%version%"
set "eulafile=%CD%\content\MC\eula.txt"

REM Crear directorio del servidor si no existe
if not exist "%serverdir%\" (
    mkdir "%serverdir%"
)

cd "%serverdir%"

REM Descargar el archivo del servidor si no existe
if not exist "%serverfile%" (
    echo Descargando %serverfile%...
    curl -o "%serverfile%" "%downloadurl%"
)

REM Ejecutar el servidor para crear archivos
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

REM Copiar el archivo eula.txt si no existe
(
echo copiando files
copy "%eulafile%" .
)
pause 
REM Ejecutar el servidor
echo Ejecutando el servidor...
java -Xmx1024M -Xms1024M -jar "%serverfile%" nogui
pause

goto :eof









:scriptold
echo Ejecutando script 1...
mkdir servers\MCvanilla\1.12.2
cd servers\MCvanilla\1.12.2
if exist "server.1.12.2.jar" (
    echo El servidor se ejecutara.
	timeout /t 3
    REM Copmandos que se ejecutaran si el archivo existe.
	java -Xmx1024M -Xms1024M -jar "server.1.12.2.jar" nogui
) else (
    echo El archivo no existe y se descargara.
    REM Comandos que se ejecutaran si el archivo no existe.
	curl -o "server.1.12.2.jar" "https://piston-data.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar"
	java -Xmx1024M -Xms1024M -jar "server.1.12.2.jar" nogui
	timeout /t 10
	cd ..
	cd ..
	cd ..
	timeout /t 3
	echo El servidor se ejecutara.
	copy "content\MC\eula.txt" "servers\MCvanilla\1.12.2"
	timeout /t 3
	cd servers\MCvanilla\1.12.2
    REM Se ejecutara el server.
	java -Xmx1024M -Xms1024M -jar "server.1.12.2.jar" nogui
	pause
)

goto :eof


:Test
	netsh advfirewall firewall add rule name="Satisfactory borrar UDP" dir=in action=allow protocol=UDP localport=27031-27036
pause
goto :menu
goto :eof






:Test_script2
echo Descargando
mkdir servers\MCForge\1.12.2
cd servers\MCForge\1.12.2
if exist "minecraft_server.1.12.2.jar" (
    echo El servidor se ejecutara.
	timeout /t 3
    REM Copmandos que se ejecutaran si el archivo existe.
	java -Xmx1024M -Xms1024M -jar "server.1.8.9.jar" nogui
) else (
    echo El archivo no existe y se descargara.
    REM Comandos que se ejecutaran si el archivo no existe.
	curl -o "server.1.12.2.Forge.jar" "https://maven.minecraftforge.net/net/minecraftforge/forge/1.12.2-14.23.5.2860/forge-1.12.2-14.23.5.2860-installer.jar"
	java -Xmx1024M -Xms1024M -jar "forge-1.12.2-14.23.5.2860-intaller.jar" nogui
	
	cd ..
	cd ..
	cd ..
	timeout /t 3
	echo El servidor se ejecutara.
	copy "content\MC\eula.txt" "servers\MCForge\1.12.2"
	timeout /t 3
	cd servers\MCvanilla\1.12.2
    REM Se ejecutara el server.
	java -Xmx1024M -Xms1024M -jar "" nogui
	pause
)

goto :eof




REM Detecta si hay un programa ejecutandose
REM		set "programa=Steam.exe"
REM		tasklist /FI "IMAGENAME eq %programa%" 2>NUL | find /I /N "%programa%">NUL
REM		if "%ERRORLEVEL%"=="0" (
REM			echo El programa %programa% está en ejecución.
REM			REM Comandos que se ejecutaran si el programa está en ejecución.
REM			
REM		) else (
REM			echo El programa %programa% no está en ejecución.
REM			REM Comandos que se ejecutaran si el programa no está en ejecución.
REM			
REM		)





:Content_Folder
REM Auto create content folder + data
echo Content

set carpeta="content"
if exist "%carpeta%\" (
    echo La carpeta %carpeta% existe.
    REM Aquí puedes poner los comandos que quieres ejecutar si la carpeta existe.
    echo Ya esta creado.
	pause
	goto :menu
) else (
    echo La carpeta %carpeta% no existe.
    REM Aquí puedes poner los comandos que quieres ejecutar si la carpeta no existe.
	echo creando
	mkdir content
	mkdir content\MC
	echo eula=true > "content\MC\eula.txt"
	goto :menu
)
goto :eof
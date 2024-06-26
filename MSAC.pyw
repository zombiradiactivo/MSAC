import os
import time
import psutil
import shutil
import ctypes
import zipfile
import requests
import threading
import subprocess
import customtkinter as ctk

# Window setup
window = ctk.CTk()
window.title('Server Creator')
window.geometry('800x400')
window.minsize(800,400)
window.maxsize(800,400)

def cerrar_aplicacion():
    # Terminar el proceso de Python
    os._exit(0)
# Al pulsar la X de la ventana se usara la funcion cerrar_aplicacion que cerrara completamente todo proceso/subproceso que siga abierto 
window.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)


# CPU and RAM progress bars setup
cpu_ram_frame = ctk.CTkFrame(window)
cpu_ram_frame.place(relx=0.75, rely=0.75, relwidth=0.2, relheight=0.25)

bar_cpu = ctk.CTkProgressBar(cpu_ram_frame, orientation='horizontal', mode='determinate')
bar_cpu.pack(expand=True, fill='both', padx=5, pady=5)

label_cpu = ctk.CTkLabel(cpu_ram_frame)
label_cpu.pack()

bar_ram = ctk.CTkProgressBar(cpu_ram_frame, orientation='horizontal', mode='determinate')
bar_ram.pack(expand=True, fill='both', padx=5, pady=5)

label_ram = ctk.CTkLabel(cpu_ram_frame)
label_ram.pack()


# Configuración del menu de la izquierda
sidebar_panel = ctk.CTkFrame(window, fg_color="transparent")
sidebar_panel.place(relx=0.05, rely=0.25, relwidth=0.2, relheight=0.5)

# Configuracion de los botones de stop
sidebar_panel2 = ctk.CTkFrame(window)
sidebar_panel2.place(relx=0.75, rely=0, relwidth=0.2, relheight=0.1)

# Configuración del menu del centro
submenu_frame = ctk.CTkFrame(window, fg_color="transparent")
submenu_frame.place(relx=0.35, rely=0.25, relwidth=0.3, relheight=0.5)

# Texto guia del menu del centro
guia_label = ctk.CTkLabel(window, text="Click Izquierdo para Iniciar | Click Derecho para Editar", fg_color="transparent")
guia_label.place(relx=0.25, rely=0.2, relwidth=0.5, relheight=0.05)
    

# Ip setup
Ip_bar = ctk.CTkFrame(window)
Ip_bar.place(relx=0.05, rely=0, relwidth=0.2, relheight=0.1) #relwidth=0.2


# Funcion para obtener la direccion ip publica 
def obtener_ip_publica():
    try:
        # Hacer una solicitud GET a ifconfig.me
        respuesta = requests.get('https://ifconfig.me/ip')
        if respuesta.status_code == 200:
            # Obtener y devolver la IP pública desde la respuesta
            ip_publica = respuesta.text.strip()
            return ip_publica
        else:
            return f'Error al obtener la IP pública. Código de estado: {respuesta.status_code}'
    except requests.RequestException as e:
        return f'Error de conexión: {e}'

ip_publica = obtener_ip_publica()

ctk.CTkLabel(Ip_bar,text=f'IP Pública: {ip_publica}').pack(expand=True, fill='both', padx=5, pady=5)



# Definir las variables globales
global Xmx4G
global Xms4G
Xmx4G = "-Xmx4G"
Xms4G = "-Xms4G"

Button_Apache = None    # Variable global para almacenar el botón Apache
Button_Filezilla = None # Variable global para almacenar el botón Filezilla


                            
                             

# Botones para la menu central

def servers_button():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='XAMPP', command=XAMPP_Installer).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Chat', command=Chat_Launcher).pack(expand=True, fill='both', padx=5, pady=5)

def games_button():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Minecraft', command=Minecraft_Loader).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Steam', command=SteamCMD_GUI_Launcher).pack(expand=True, fill='both', padx=5, pady=5)

# Botones para la menu de la izquierda
ctk.CTkButton(sidebar_panel, text='Servidores', command=servers_button).pack(expand=True, fill='both', padx=5, pady=5)
ctk.CTkButton(sidebar_panel, text='Juegos', command=games_button).pack(expand=True, fill='both', padx=5, pady=5)







# Submenú de funciones de servidores
def Xampp_Menu():
    for widget in submenu_frame.winfo_children():
        widget.destroy()

    # Botones para submenú
    #Button_Configurar = ctk.CTkButton(submenu_frame, text='Configurar', command=Apache_Start)
    #Button_Configurar.pack(expand=True, fill='both', padx=5, pady=5)

    global Button_Apache
    Button_Apache = ctk.CTkButton(submenu_frame, text='Apache', command=Apache_Start)
    Button_Apache.pack(expand=True, fill='both', padx=5, pady=5)
    Button_Apache.bind("<Button-3>", lambda event : Xampp_Apache_menu(event))
    global Button_Filezilla
    Button_Filezilla = ctk.CTkButton(submenu_frame, text='Filezilla', command=Filezilla_Start)
    Button_Filezilla.pack(expand=True, fill='both', padx=5, pady=5)

def Xampp_Apache_menu(event):
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    Button_Apache_Folder = ctk.CTkButton(submenu_frame, text='Carpeta', command = Xampp_folder)
    Button_Apache_Folder.pack(expand=True, fill='both', padx=5, pady=5)
    Button_Apache_httpd_conf = ctk.CTkButton(submenu_frame, text='httpd.conf',command=lambda: (Xampp_Text_Editor("httpd.conf")))
    Button_Apache_httpd_conf.pack(expand=True, fill='both', padx=5, pady=5)
    Button_Apache_httpd_ssl_conf = ctk.CTkButton(submenu_frame, text='httpd-ssl.conf',command=lambda: (Xampp_Text_Editor("httpd-ssl.conf")))
    Button_Apache_httpd_ssl_conf.pack(expand=True, fill='both', padx=5, pady=5)
    Button_Apache_httpd_xampp_conf = ctk.CTkButton(submenu_frame, text='httpd-xampp.conf',command=lambda: (Xampp_Text_Editor("httpd-xampp.conf")))
    Button_Apache_httpd_xampp_conf.pack(expand=True, fill='both', padx=5, pady=5)
    Button_Apache_php_ini = ctk.CTkButton(submenu_frame, text='php.ini',command=lambda: (Xampp_Text_Editor("php.ini")))
    Button_Apache_php_ini.pack(expand=True, fill='both', padx=5, pady=5)
    Button_Apache_config_inc_php = ctk.CTkButton(submenu_frame, text='config.inc.php',command=lambda: (Xampp_Text_Editor("config.inc.php")))
    Button_Apache_config_inc_php.pack(expand=True, fill='both', padx=5, pady=5)

def Xampp_Text_Editor(version):
    # Ruta del archivo a editar
    
    if version == "httpd.conf":
        ruta_archivo = "C:\\xampp\\apache\\conf\\httpd.conf"
    if version == "httpd-ssl.conf":
        ruta_archivo = "C:\\xampp\\apache\\conf\\extra\\httpd-ssl.conf"
    if version == "httpd-xampp.conf":
        ruta_archivo = "C:\\xampp\\apache\\conf\\extra\\httpd-xampp.conf"
    if version == "php.ini":
        ruta_archivo = "C:\\xampp\\php\\php.ini"
    if version == "config.inc.php":
        ruta_archivo = "C:\\xampp\\phpMyAdmin\\config.inc.php"
    

    # Crear una nueva ventana
    ventana_editor = ctk.CTkToplevel()
    ventana_editor.title(f"Editor de {version}")
    ventana_editor.geometry('800x400')
    ventana_editor.minsize(800,400)

    # Crear un área de texto
    texto_editor = ctk.CTkTextbox(ventana_editor, wrap='word', width=60, height=20)
    texto_editor.pack(expand=True, fill='both', side='left')
    
    # Cargar el contenido del archivo en el área de texto
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            texto_editor.insert('end', contenido)
    except FileNotFoundError:
        contenido = ""
    
    # Función para guardar el archivo
    def guardar():
        contenido = texto_editor.get("1.0", 'end')
        guardar_archivo(ruta_archivo, contenido)
    
    # Botón para guardar cambios
    boton_guardar = ctk.CTkButton(ventana_editor, text="Guardar", command=guardar)
    boton_guardar.pack(side='bottom')
    
    # Función para cerrar la ventana
    def cerrar_ventana():
        ventana_editor.destroy()
    
    # Botón para cerrar la ventana
    boton_cerrar = ctk.CTkButton(ventana_editor, text="Cerrar", command=cerrar_ventana)
    boton_cerrar.pack(side='bottom')

def Xampp_folder():
    print ("hola")


# Funcion para instalar la version 8.2.12 de xampp sino esta instalada o  abrir el menu de xampp
def XAMPP_Installer():
    url_archivo = 'https://netcologne.dl.sourceforge.net/project/xampp/XAMPP%20Windows/8.2.12/xampp-windows-x64-8.2.12-0-VS16-installer.exe'
    nombre_local = 'XAMPP.exe'
    ruta_carpeta_descarga = 'temp/xampp'
    ruta_instalador = 'temp/xampp/xampp.exe'
    ruta_archivo_indicador = 'C:/xampp/xampp-control.exe'

    def verificar_xampp_instalado():
        return os.path.exists(ruta_archivo_indicador)

    def descargar_instalar_xampp():
        # Crear un hilo para la descarga del archivo
        def descargar():
            descargar_archivo(url_archivo, nombre_local, ruta_carpeta_descarga)
            # Comando para ejecutar el instalador
            cmd = f'powershell.exe -Command "Start-Process \'{ruta_instalador}\' -Verb runAs"'
            subprocess.run(cmd, shell=True)

        threading.Thread(target=descargar).start()
        
    
    # Llamada a la función
    xampp_instalado = verificar_xampp_instalado()  
    

    # Puedes usar la variable xampp_instalado para tomar decisiones en tu aplicación
    if xampp_instalado:
        # XAMPP está instalado
        print("XAMPP está instalado.")
        Xampp_Menu()  # Llamada a la función Xampp_Menu
    else:
        # XAMPP no está instalado
        print("XAMPP no está instalado.")
        descargar_instalar_xampp()



# Funcion para parar el servidor de Apache
def Apache_Start():
    global Button_Apache
    Apache_Start_Exe = 'C:/xampp/apache/bin/httpd.exe'
    Button_Stop_Apache = ctk.CTkButton(sidebar_panel2, text='Stop Apache', command=lambda: (Apache_Stop(process, Button_Stop_Apache)))
    Button_Stop_Apache.pack(expand=True, fill='both', padx=5, pady=5)
    cmd = f'powershell.exe Start-Process "{Apache_Start_Exe}"'  # Start Apache server
    process = subprocess.Popen(cmd, shell=False)
    
    if Button_Apache:
        Button_Apache.configure(state="disabled")
    
   # Espera a que se inicie el servidor Apache
    process.wait()

# Funcion para parar el servidor de Apache
def Apache_Stop(process, button):
    global Button_Apache
    if button:
        button.destroy()
    # Obtiene una lista de todos los procesos en ejecución
    processes = psutil.process_iter()
    
    if Button_Apache:
        Button_Apache.configure(state="enabled")
    
    # Procesa la lista de procesos
    for process in processes:
        # Comprueba si el proceso tiene el nombre "httpd.exe"
        if process.name() == "httpd.exe":
            # Finaliza el proceso
            process.kill()



# Funcion para iniciar el servidor de Filezilla
def Filezilla_Start():
    global Button_Filezilla
    Filezilla_Start_Exe = 'C:/xampp/FileZillaFTP/FileZillaServer.exe'
    Button_Stop_Filezilla = ctk.CTkButton(sidebar_panel2, text='Stop Filezilla', command=lambda: (Filezilla_Stop(process, Button_Stop_Filezilla)))
    Button_Stop_Filezilla.pack(expand=True, fill='both', padx=5, pady=5)
    cmd = f'powershell.exe Start-Process "{Filezilla_Start_Exe}"'  
    process = subprocess.Popen(cmd, shell=False)
    
    if Button_Filezilla:
        Button_Filezilla.configure(state="disabled")
    
    process.wait()

# Funcion para parar el servidor de Filezilla
def Filezilla_Stop(process, button):
    global Button_Filezilla
    if button:
        button.destroy()
    processes = psutil.process_iter()
    
    if Button_Filezilla:
        Button_Filezilla.configure(state="enabled")
    
    for process in processes:

        if process.name() == "FileZillaServer.exe":
            process.kill()

# Funcion para iniciar Server_Chat.pyw 
def Chat_Launcher():
    # Carga la biblioteca de sistema
    shell32 = ctypes.windll.shell32

    # Ruta de la aplicación 
    app_path = "Server_Chat.pyw"

    # Llama a la función ShellExecuteW de la biblioteca shell32
    # Esta función abre un archivo o ejecutable, como lo haría el explorador de Windows.
    # La función devuelve un valor entero que indica si se pudo abrir la aplicación.
    result = shell32.ShellExecuteW(None, "open", app_path, None, None, 1)

    # Si el resultado es mayor que 32, significa que se ha abierto correctamente
    if result > 32:
        print("La aplicación se abrió correctamente.")
    else:
        print("Error al abrir la aplicación.")

# Funcion para iniciar SteamCMD_GUI.py 
def SteamCMD_GUI_Launcher():

    shell32 = ctypes.windll.shell32

    app_path = "SteamCMD_GUI.pyw"

    result = shell32.ShellExecuteW(None, "open", app_path, None, None, 1)

    if result > 32:
        print("La aplicación se abrió correctamente.")
    else:
        print("Error al abrir la aplicación.")




# Menu de selector del Minecraft Loader (Con o sin Mods) 
def Minecraft_Loader():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Minecraft Vanilla', command=Minecraft_Vanilla).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Minecraft Forge',   command=Minecraft_Forge).pack(expand=True, fill='both', padx=5, pady=5)

# Menu Vanilla
#
def Minecraft_Vanilla():
    for widget in submenu_frame.winfo_children():
        widget.destroy()

    submenu_scroleableframe = ctk.CTkScrollableFrame(submenu_frame, fg_color="transparent")
    submenu_scroleableframe.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Botones para submenú
    boton_1_20_1 = ctk.CTkButton(submenu_scroleableframe, text='1.20.2', command=descargar_1_20_2)
    boton_1_20_1.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_20_1.bind("<Button-3>", lambda event, version="1.20.1": click_derecho(event, version))
    
    boton_1_19_4= ctk.CTkButton(submenu_scroleableframe, text='1.19.4', command=descargar_1_19_4)
    boton_1_19_4.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_19_4.bind("<Button-3>", lambda event, version="1.19.4": click_derecho(event, version))
    
    boton_1_18_2 = ctk.CTkButton(submenu_scroleableframe, text='1.18.2', command=descargar_1_18_2)
    boton_1_18_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_18_2.bind("<Button-3>", lambda event, version="1.18.2": click_derecho(event, version))

    boton_1_17_1 = ctk.CTkButton(submenu_scroleableframe, text='1.17.1', command=descargar_1_17_1)
    boton_1_17_1.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_17_1.bind("<Button-3>", lambda event, version="1.17.1": click_derecho(event, version))

    boton_1_16_5 = ctk.CTkButton(submenu_scroleableframe, text='1.16.5', command=descargar_1_16_5)
    boton_1_16_5.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_16_5.bind("<Button-3>", lambda event, version="1.16.5": click_derecho(event, version))

    boton_1_15_2 = ctk.CTkButton(submenu_scroleableframe, text='1.15.2', command=descargar_1_15_2)
    boton_1_15_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_15_2.bind("<Button-3>", lambda event, version="1.15.2": click_derecho(event, version))

    boton_1_14_4 = ctk.CTkButton(submenu_scroleableframe, text='1.14.4', command=descargar_1_14_4)
    boton_1_14_4.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_14_4.bind("<Button-3>", lambda event, version="1.14.4": click_derecho(event, version))

    boton_1_13_2 = ctk.CTkButton(submenu_scroleableframe, text='1.13.2', command=descargar_1_13_2)
    boton_1_13_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_13_2.bind("<Button-3>", lambda event, version="1.13.2": click_derecho(event, version))

    boton_1_12_2 = ctk.CTkButton(submenu_scroleableframe, text='1.12.2', command=descargar_1_12_2)
    boton_1_12_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_12_2.bind("<Button-3>", lambda event, version="1.12.2": click_derecho(event, version))

    boton_1_11_2 = ctk.CTkButton(submenu_scroleableframe, text='1.11.2',  command=descargar_1_11_2)
    boton_1_11_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_11_2.bind("<Button-3>", lambda event, version="1.11.2": click_derecho(event, version))

    boton_1_10_2 = ctk.CTkButton(submenu_scroleableframe, text='1.10.2',  command=descargar_1_10_2)
    boton_1_10_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_10_2.bind("<Button-3>", lambda event, version="1.10.2": click_derecho(event, version))
    
    boton_1_9_4 = ctk.CTkButton(submenu_scroleableframe, text='1.9.4',   command=descargar_1_9_4)
    boton_1_9_4.pack(expand=True, fill='both', padx=5, pady=5)
    boton_1_9_4.bind("<Button-3>", lambda event, version="1.9.4": click_derecho(event, version))
    


# Funciones de los botones del Menu Vanilla 
#
def descargar_1_20_2():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/5b868151bd02b41319f54c8d4061b8cae84e665c/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_20_2.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.20.2'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_19_4():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_19_4.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.19.4'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_18_2():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_18_2.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.18.2'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_17_1():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_17_1.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.17.1'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_16_5():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_16_5.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.16.5'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_15_2():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/bb2b6b1aefcd70dfd1892149ac3a215f6c636b07/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_15_2.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.15.2'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_14_4():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/3dc3d84a581f14691199cf6831b71ed1296a9fdf/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_14_4.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.14.4'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_13_2():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/3737db93722a9e39eeada7c27e7aca28b144ffa7/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_13_2.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.13.2'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_12_2():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_12_2.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.12.2'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_11_2():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/f00c294a1576e03fddcac777c3cf4c7d404c4ba4/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_11_2.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.11.2'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_10_2():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/3d501b23df53c548254f5e3f66492d178a48db63/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_10_2.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.10.2'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()

def descargar_1_9_4():
    # URL del archivo a descargar
    url_archivo = 'https://piston-data.mojang.com/v1/objects/edbb7b1758af33d365bf835eb9d13de005b1e274/server.jar'
    # Nombre con el que se guardará el archivo descargado localmente
    nombre_local = 'server_1_9_4.jar'
    # Nombre del archivo eula
    nombre_eula = 'eula.txt'
    # Carpeta donde se guardará el archivo descargado
    ruta_carpeta = 'Main/MCvanilla/1.19.4'
    # Crear la ruta completa donde se guardará el archivo descargado
    ruta_completa_eula = os.path.join(ruta_carpeta, nombre_eula)
    # Número de la línea que deseas editar
    numero_linea = 3
    # Nuevo contenido para escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()



# Menu de Forge
#
def Minecraft_Forge():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    
    submenu_scroleableframe = ctk.CTkScrollableFrame(submenu_frame, fg_color="transparent")
    submenu_scroleableframe.place(relx=0, rely=0, relwidth=1, relheight=1)
    # Botones para submenú
    boton_forge_1_20_1 = ctk.CTkButton(submenu_scroleableframe, text='1.20.1', command=descargar_forge_1_20_1)
    boton_forge_1_20_1.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_20_1.bind("<Button-3>", lambda event, version="1.20.1": click_derecho_forge(event, version))
    
    boton_forge_1_19_4 = ctk.CTkButton(submenu_scroleableframe, text='1.19.4', command=descargar_forge_1_19_4)
    boton_forge_1_19_4.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_19_4.bind("<Button-3>", lambda event, version="1.19.4": click_derecho_forge(event, version))
    
    boton_forge_1_18_2 = ctk.CTkButton(submenu_scroleableframe, text='1.18.2', command=descargar_forge_1_18_2)
    boton_forge_1_18_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_18_2.bind("<Button-3>", lambda event, version="1.18.2": click_derecho_forge(event, version))
    
    boton_forge_1_17_1 = ctk.CTkButton(submenu_scroleableframe, text='1.17.1', command=descargar_forge_1_17_1)
    boton_forge_1_17_1.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_17_1.bind("<Button-3>", lambda event, version="1.17.1": click_derecho_forge(event, version))
    
    boton_forge_1_16_5 = ctk.CTkButton(submenu_scroleableframe, text='1.16.5', command=descargar_forge_1_16_5)
    boton_forge_1_16_5.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_16_5.bind("<Button-3>", lambda event, version="1.16.5": click_derecho_forge(event, version))
    
    boton_forge_1_15_2 = ctk.CTkButton(submenu_scroleableframe, text='1.15.2', command=descargar_forge_1_15_2)
    boton_forge_1_15_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_15_2.bind("<Button-3>", lambda event, version="1.15.2": click_derecho_forge(event, version))
    
    boton_forge_1_14_4 = ctk.CTkButton(submenu_scroleableframe, text='1.14.4', command=descargar_forge_1_14_4)
    boton_forge_1_14_4.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_14_4.bind("<Button-3>", lambda event, version="1.14.4": click_derecho_forge(event, version))
    
    boton_forge_1_13_2 = ctk.CTkButton(submenu_scroleableframe, text='1.13.2', command=descargar_forge_1_13_2)
    boton_forge_1_13_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_13_2.bind("<Button-3>", lambda event, version="1.13.2": click_derecho_forge(event, version))
    
    boton_forge_1_12_2 = ctk.CTkButton(submenu_scroleableframe, text='1.12.2', command=descargar_forge_1_12_2)
    boton_forge_1_12_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_12_2.bind("<Button-3>", lambda event, version="1.12.2": click_derecho_forge(event, version))
    
    boton_forge_1_11_2 = ctk.CTkButton(submenu_scroleableframe, text='1.11.2', command=descargar_forge_1_11_2)
    boton_forge_1_11_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_11_2.bind("<Button-3>", lambda event, version="1.11.2": click_derecho_forge(event, version))
    
    boton_forge_1_10_2 = ctk.CTkButton(submenu_scroleableframe, text='1.10.2', command=descargar_forge_1_10_2)
    boton_forge_1_10_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_10_2.bind("<Button-3>", lambda event, version="1.10.2": click_derecho_forge(event, version))
    
    boton_forge_1_9_4 = ctk.CTkButton(submenu_scroleableframe, text='1.9.4',  command=descargar_forge_1_9_4)
    boton_forge_1_9_4.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_9_4.bind("<Button-3>", lambda event, version="1.9.4": click_derecho_forge(event, version))
    
    boton_forge_1_8_9 = ctk.CTkButton(submenu_scroleableframe, text='1.8.9',  command=descargar_forge_1_8_9)
    boton_forge_1_8_9.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_8_9.bind("<Button-3>", lambda event, version="1.8.9": click_derecho_forge(event, version))
    
    boton_forge_1_7_10 = ctk.CTkButton(submenu_scroleableframe, text='1.7.10', command=descargar_forge_1_7_10)
    boton_forge_1_7_10.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_7_10.bind("<Button-3>", lambda event, version="1.7.10": click_derecho_forge(event, version))
    
    boton_forge_1_6_4 = ctk.CTkButton(submenu_scroleableframe, text='1.6.4',  command=descargar_forge_1_6_4)
    boton_forge_1_6_4.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_6_4.bind("<Button-3>", lambda event, version="1.6.4": click_derecho_forge(event, version))
    
    boton_forge_1_5_2 = ctk.CTkButton(submenu_scroleableframe, text='1.5.2',  command=descargar_forge_1_5_2)
    boton_forge_1_5_2.pack(expand=True, fill='both', padx=5, pady=5)
    boton_forge_1_5_2.bind("<Button-3>", lambda event, version="1.5.2": click_derecho_forge(event, version))



# Funciones de los botones del Menu Forge 
#
def descargar_forge_1_20_1():

    ruta_carpeta = 'Main/MCForge/1.20.1'
    nombre_local = "forge_1.20.1.jar"
    type = "modded"
    category = "forge"
    version = "1.20.1"
    ejecutable_modificado = "@user_jvm_args.txt @libraries/net/minecraftforge/forge/1.20.1-47.2.30/win_args.txt %*"
    ejecutable = "run.bat"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)  

    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_19_4():

    ruta_carpeta = 'Main/MCForge/1.19.4'
    nombre_local = "forge_1.19.4.jar"
    type = "modded"
    category = "forge"
    version = "1.19.4"
    ejecutable = "run.bat"
    ejecutable_modificado = " @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.19.4-45.2.15/win_args.txt %*"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_18_2():

    ruta_carpeta = 'Main/MCForge/1.18.2'
    nombre_local = "forge_1.18.2.jar"
    type = "modded"
    category = "forge"
    version = "1.18.2"
    ejecutable = "run.bat"
    ejecutable_modificado = " @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.18.2-40.2.18/win_args.txt %*"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_17_1():

    ruta_carpeta = 'Main/MCForge/1.17.1'
    nombre_local = "forge_1.17.1.jar"
    type = "modded"
    category = "forge"
    version = "1.17.1"
    ejecutable = "run.bat"
    ejecutable_modificado = " @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.17.1-45.2.15/win_args.txt %*"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_16_5():

    ruta_carpeta = 'Main/MCForge/1.16.5'
    nombre_local = "forge_1.16.5.jar"
    type = "modded"
    category = "forge"
    version = "1.16.5"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    print(ejecutable_modificado)
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_15_2():

    ruta_carpeta = 'Main/MCForge/1.15.2'
    nombre_local = "forge_1.15.2.jar"
    type = "modded"
    category = "forge"
    version = "1.15.2"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_14_4():

    ruta_carpeta = 'Main/MCForge/1.14.4'
    nombre_local = "forge_1.14.4.jar"
    type = "modded"
    category = "forge"
    version = "1.14.4"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_13_2():

    ruta_carpeta = 'Main/MCForge/1.13.2'
    nombre_local = "forge_1.13.2.jar"
    type = "modded"
    category = "forge"
    version = "1.13.2"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_12_2():

    ruta_carpeta = 'Main/MCForge/1.12.2'
    nombre_local = "forge_1.12.2.jar"
    type = "modded"
    category = "forge"
    version = "1.12.2"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_11_2():

    ruta_carpeta = 'Main/MCForge/1.11.2'
    nombre_local = "forge_1.11.2.jar"
    type = "modded"
    category = "forge"
    version = "1.11.2"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_10_2():

    ruta_carpeta = 'Main/MCForge/1.10.2'
    nombre_local = "forge_1.10.2.jar"
    type = "modded"
    category = "forge"
    version = "1.10.2"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_9_4():

    ruta_carpeta = 'Main/MCForge/1.9.4'
    nombre_local = "forge_1.9.4.jar"
    type = "modded"
    category = "forge"
    version = "1.9.4"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_8_9():

    ruta_carpeta = 'Main/MCForge/1.8.9'
    nombre_local = "forge_1.8.9.jar"
    type = "modded"
    category = "forge"
    version = "1.8.9"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_7_10():

    ruta_carpeta = 'Main/MCForge/1.7.10'
    nombre_local = "forge_1.7.10.jar"
    type = "modded"
    category = "forge"
    version = "1.7.10"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_6_4():

    ruta_carpeta = 'Main/MCForge/1.6.4'
    nombre_local = "forge_1.6.4.jar"
    type = "modded"
    category = "forge"
    version = "1.6.4"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_5_2():

    ruta_carpeta = 'Main/MCForge/1.5.2'
    nombre_local = "forge_1.5.2.jar"
    type = "modded"
    category = "forge"
    version = "1.5.2"
    ejecutable = f"minecraft_server.{version}.jar"
    global Xmx4G
    global Xms4G
    ejecutable_modificado = f"-jar {ejecutable} {Xmx4G} {Xms4G}"
    java_JDK_22 = "Data\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        descargar_java_jdk_22()
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()




# Funciones para Forge 
#
# Funcion que permite el Click derecho el los botones del Menu de Forge 
def click_derecho_forge(event, version):
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Editar server.propeties',  command=lambda: (editar_server_propeties_forge(version))).pack(expand=True, fill='both', padx=5, pady=5)
    # Si la version es una de las siguientes habilitar el boton para el editor de texto sino habilitar un slider para seleccionar la memoria RAM 
    if version in ["1.20.1", "1.19.4", "1.18.2", "1.17.1"]:
        ctk.CTkButton(submenu_frame, text='Editar uso de RAM', command=lambda: (editar_RAM_forge_user_jvm_args(version))).pack(expand=True, fill='both', padx=5, pady=5)
    else:
        Button_Ram = ctk.CTkButton(submenu_frame, text='Editar uso de RAM', command=lambda: (editar_RAM_forge_user_jvm_args(version)))
        Button_Ram.pack(expand=False, fill='both', padx=5, pady=5)
        Button_Ram.configure(state="disabled")
        def on_slider_change(value):
            editar_configuracion_de_memoria(f"{value}G")

        slider = ctk.CTkSlider(submenu_frame, from_=4, to=16, number_of_steps=6, width=100, height=10, command=on_slider_change)
        slider.pack(expand=False, fill='both', padx=5, pady=5)
        slider.set(4)  

# Funcion para editar el archivo server.properties que se encarga de la configuracion del servidor como la dificultad del juego, modo de juego, nombre del mundo, semilla del mundo, etc...
def editar_server_propeties_forge(version):
    # Ruta del archivo a editar
    ruta_archivo = f"Main/MCForge/{version}/server.properties"
    
    # Crear una nueva ventana
    ventana_editor = ctk.CTkToplevel()
    ventana_editor.title("Editor de server.properties")
    ventana_editor.geometry('800x400')
    ventana_editor.minsize(800,400)

    # Crear un área de texto
    texto_editor = ctk.CTkTextbox(ventana_editor, wrap='word', width=60, height=20)
    texto_editor.pack(expand=True, fill='both', side='left')
    
    # Cargar el contenido del archivo en el área de texto
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            texto_editor.insert('end', contenido)
    except FileNotFoundError:
        contenido = ""
    
    # Función para guardar el archivo
    def guardar():
        contenido = texto_editor.get("1.0", 'end')
        guardar_archivo(ruta_archivo, contenido)
    
    # Botón para guardar cambios
    boton_guardar = ctk.CTkButton(ventana_editor, text="Guardar", command=guardar)
    boton_guardar.pack(side='bottom')
    
    # Función para cerrar la ventana
    def cerrar_ventana():
        ventana_editor.destroy()
    
    # Botón para cerrar la ventana
    boton_cerrar = ctk.CTkButton(ventana_editor, text="Cerrar", command=cerrar_ventana)
    boton_cerrar.pack(side='bottom')

# Funcion para editar el archivo user_jvm_args que se encarga de almacenar la cantidad de ram que el servidor usara
def editar_RAM_forge_user_jvm_args(version):
    
    # Edita la ram desde la version 1.20.1 hasta 1.17.1
    ruta_archivo = f"Main/MCForge/{version}/user_jvm_args.txt"
    print("Editando ram")
    
    # Crear una nueva ventana
    ventana_editor = ctk.CTkToplevel()
    ventana_editor.title("Editor de user_jvm_args")
    ventana_editor.geometry('800x400')
    ventana_editor.minsize(800,400)

    # Crear un área de texto
    texto_editor = ctk.CTkTextbox(ventana_editor, wrap='word', width=60, height=20)
    texto_editor.pack(expand=True, fill='both', side='left')
    
    # Cargar el contenido del archivo en el área de texto
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            texto_editor.insert('end', contenido)
    except FileNotFoundError:
        contenido = ""
    
    # Función para guardar el archivo
    def guardar():
        contenido = texto_editor.get("1.0", 'end')
        guardar_archivo(ruta_archivo, contenido)
    
    # Botón para guardar cambios
    boton_guardar = ctk.CTkButton(ventana_editor, text="Guardar", command=guardar)
    boton_guardar.pack(side='bottom')
    
    # Función para cerrar la ventana
    def cerrar_ventana():
        ventana_editor.destroy()
    
    # Botón para cerrar la ventana
    boton_cerrar = ctk.CTkButton(ventana_editor, text="Cerrar", command=cerrar_ventana)
    boton_cerrar.pack(side='bottom')

# Funcion para editar la cantidad de memoria que usara el sevidor de forge 
def editar_configuracion_de_memoria(Xmx):
    global Xmx4G
    global Xms4G
    Xmx4G = f"-Xmx{Xmx}"
    Xms4G = f"-Xms{Xmx}"
    print(Xms4G)

# Funcion para el primer inicio del la instancia del servidor para que cree los archivos necesarios
def first_run_forge(ruta_carpeta, ejecutable, java_JDK_22, ejecutable_modificado):
    nombre_eula = 'eula.txt'
    ruta_completa = os.path.join(ruta_carpeta, nombre_eula)
    try:
        # Si no existe en la carpeta el archivo eula.txt 
        if not os.path.exists(ruta_completa):
            
            if ejecutable == "run.bat":
                # Comando a ejecutar si el ejecutable es "run.bat"
                comando = f'"{java_JDK_22}" {ejecutable_modificado}'
            else:
                # Comando a ejecutar si el ejecutable no es "run.bat"
                comando = ejecutable
    
        try:
            subprocess.run(comando, shell=True, cwd=ruta_carpeta)
        except Exception as e:
            print(f"Error al ejecutar el comando: {e}")

    except Exception as e:
        print(f"Error al gestionar el servidor Forge: {e}")

# Funcion que servira para descargar, instalar o ejecutar el servidor de Forge seleccionado 
def download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version):
    try:

        ruta_absoluta = os.path.abspath(os.path.join(ruta_carpeta, nombre_local))
        ruta_ejecutable = os.path.abspath(os.path.join(ruta_carpeta, ejecutable))
        ruta_eula= os.path.join(ruta_carpeta, "eula.txt")
        
        # Verificar si el archivo .jar ya está descargado
        print (ruta_absoluta)
        if not os.path.exists(ruta_absoluta):
            print("Descargando servidor Forge...")
            API_SERVERJARS_descargar_jar(type, category, version, ruta_carpeta)     #Descarga .jar

        # Verificar si el servidor ya está instalado
        if not os.path.exists(ruta_ejecutable):
            print("Instalando servidor Forge...")
            install_forge(ruta_carpeta, nombre_local)       #Ejecuta .jar deja .bat

        if not os.path.exists(ruta_eula):
            print("Primera Ejecucion")
            first_run_forge(ruta_carpeta, ejecutable, java_JDK_22, ejecutable_modificado)      #Ejecuta .jar deja .jar 
            time.sleep(5)

        print("Editar EULA")
        editar_eula(ruta_carpeta)       # Comprueba si editar o no


        # Ejecutar el servidor
        print("Ejecutando servidor Forge...")
        if ejecutable == "run.bat":
            # Comando a ejecutar si el ejecutable es "run.bat"
            ruta_java= os.path.abspath(java_JDK_22)
            print (ruta_java)
            comando = f'"{ruta_java}" {ejecutable_modificado}'
        else:
            # Comando a ejecutar si el ejecutable no es "run.bat"
            comando = ejecutable
    
        try:
            subprocess.run(comando, shell=True, cwd=ruta_carpeta)
        except Exception as e:
            print(f"Error al ejecutar el comando: {e}")
    except Exception as e:
        print(f"Error al gestionar el servidor Forge: {e}")

# Funcion para instalar el servidor de Forge
def install_forge(ruta_carpeta, nombre_local):
    try:
        # Obtener la ruta absoluta al archivo .jar
        ruta_absoluta = os.path.abspath(os.path.join(ruta_carpeta, nombre_local))

        # Comando para ejecutar el archivo .jar usando Java
        comando = f"java -jar {nombre_local} --installServer"

        # Ejecutar el archivo .jar
        subprocess.run(comando, shell=True, cwd=ruta_carpeta)
    except Exception as e:
        print(f"Error al ejecutar el archivo .jar: {e} {ruta_absoluta}")


#####

# Función para descargar un archivo JAR específico de un tipo y categoría con una versión determinada a traves de la API serverjars.com
def API_SERVERJARS_descargar_jar(type, category, version, carpeta):
    nombre_archivo = f"{category}_{version}.jar"
    url = f"https://api.serverjars.com/api/fetchJar/{type}/{category}/{version}"
    
    try:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        
        if not os.path.exists(ruta_completa):
            with requests.get(url, stream=True) as respuesta:
                total_size = int(respuesta.headers.get('content-length', 0))
                chunk_size = 8192  # Tamaño del chunk
                received_bytes = 0
                
                # Crear la barra de progreso
                progress_bar = ctk.CTkProgressBar(window, orientation='horizontal', mode='determinate')
                progress_bar.place(relx=0, rely=1, relwidth=1, anchor='sw')

                with open(ruta_completa, 'wb') as archivo:
                    for data in respuesta.iter_content(chunk_size=chunk_size):
                        received_bytes += len(data)
                        archivo.write(data)
                        if total_size > 0:
                            percent_complete = received_bytes / total_size * 100
                            # Actualizar la barra de progreso cada 5%
                            if percent_complete % 5 == 0:
                                print(f"Descargado: {percent_complete:.2f}%")
                                
            print(f"Descarga de '{nombre_archivo}' completada en '{carpeta}'")
            # Destruir la barra de progreso al finalizar la descarga
            progress_bar.destroy()
        else:
            print(f"'{nombre_archivo}' ya existe en '{carpeta}', no es necesario descargarlo nuevamente.")
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")

# Funcion para descargar un archivo segun una url dada
def descargar_archivo(url, nombre_archivo, carpeta):
    try:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        
        if not os.path.exists(ruta_completa):
            with requests.get(url, stream=True) as respuesta:
                total_size = int(respuesta.headers.get('content-length', 0))
                chunk_size = 8192  # Tamaño del chunk
                received_bytes = 0
            
                download_progress_bar = ctk.CTkProgressBar(window, mode='determinate')
                download_progress_bar.place(relx=0, rely=1, relwidth=1, anchor='sw')

                with open(ruta_completa, 'wb') as archivo:
                    for data in respuesta.iter_content(chunk_size=chunk_size):
                        received_bytes += len(data)
                        archivo.write(data)
                        percent_complete = round((received_bytes / total_size)* 100, 1)
                        percent_complete_bar = round(((received_bytes / total_size)), 3)
                        print(f"{percent_complete_bar} bar")
                        print(f"{percent_complete} no")
                        if percent_complete % 1 == 0:
                            download_progress_bar.set(percent_complete_bar)                            

            print(f"Descarga de '{nombre_archivo}' completada en '{carpeta}'")
            # Destruir la barra de progreso al finalizar la descarga
            download_progress_bar.destroy()
        else:
            print(f"'{nombre_archivo}' ya existe en '{carpeta}', no es necesario descargarlo nuevamente.")
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")

# Funcion para ejecutar un servidor de Minecraft Vanilla 
def ejecutar_jar(ruta_carpeta, nombre_local):
        global Xmx4G
        global Xms4G
        try:
            # Obtener la ruta absoluta al archivo .jar
            ruta_absoluta = os.path.abspath(os.path.join(ruta_carpeta))

            # Comando para ejecutar el archivo .jar usando Java
            comando = f"java {Xmx4G} {Xms4G} -jar {nombre_local}"

            # Ejecutar el archivo .jar
            subprocess.run(comando, shell=True, cwd=ruta_absoluta)
        except Exception as e:
            print(f"Error al ejecutar el archivo .jar: {e} {ruta_absoluta}")

# Funcion que permite el Click derecho el los botones del Menu de Forge 
def click_derecho(event, version):
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Editar server.propeties',  command=lambda: (editar_server_propeties(version))).pack(expand=False, fill='both', padx=5, pady=5)

    RAM_value = ctk.CTkLabel(submenu_frame, text=f"Cantidad de RAM : {Xms4G}")
    RAM_value.pack(fill='both', padx=5, pady=5)

    def on_slider_change(value):
        RAM_value.configure(text=f"Cantidad de RAM : {Xms4G}")
        editar_configuracion_de_memoria(f"{value}G")
    slider = ctk.CTkSlider(submenu_frame, from_=2, to=16, number_of_steps=7, width=100, height=10, command=on_slider_change)
    slider.pack(expand=False, fill='both', padx=5, pady=5)
    slider.set(4)
    

# Funcion para editar el archivo server.properties que se encarga de la configuracion del servidor como la dificultad del juego, modo de juego, nombre del mundo, semilla del mundo, etc...
def editar_server_propeties(version):
    # Ruta del archivo a editar
    ruta_archivo = f"Main/MC/{version}/server.properties"
    
    # Crear una nueva ventana
    ventana_editor = ctk.CTkToplevel()
    ventana_editor.title("Editor de server.properties")
    ventana_editor.geometry('800x400')
    ventana_editor.minsize(800,400)

    # Crear un área de texto
    texto_editor = ctk.CTkTextbox(ventana_editor, wrap='word', width=60, height=20)
    texto_editor.pack(expand=True, fill='both', side='left')
    
    # Cargar el contenido del archivo en el área de texto
    try:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            texto_editor.insert('end', contenido)
    except FileNotFoundError:
        contenido = ""
    
    # Función para guardar el archivo
    def guardar():
        contenido = texto_editor.get("1.0", 'end')
        guardar_archivo(ruta_archivo, contenido)
    
    # Botón para guardar cambios
    boton_guardar = ctk.CTkButton(ventana_editor, text="Guardar", command=guardar)
    boton_guardar.pack(side='bottom')
    
    # Función para cerrar la ventana
    def cerrar_ventana():
        ventana_editor.destroy()
    
    # Botón para cerrar la ventana
    boton_cerrar = ctk.CTkButton(ventana_editor, text="Cerrar", command=cerrar_ventana)
    boton_cerrar.pack(side='bottom')

# Funcion para borrar una carpeta segun una ruta dada
def borrar_carpeta(ruta_carpeta):
    try:
        # Borra la carpeta y su contenido de manera recursiva
        shutil.rmtree(ruta_carpeta)
        print(f"Carpeta '{ruta_carpeta}' y su contenido han sido eliminados correctamente.")
    except OSError as e:
        print(f"Error al borrar la carpeta '{ruta_carpeta}': {e}")

# Funcion para editar la tercera linea de el archivo eula.txt segun una ruta dada
def editar_eula(ruta_carpeta):
    nombre_eula = 'eula.txt'
    numero_linea = 3  # Número de línea a editar
    nuevo_contenido = "eula=true"
    ruta_completa = os.path.join(ruta_carpeta, nombre_eula)
    
    try:
        with open(ruta_completa, 'r') as archivo:
            lineas = archivo.readlines()
        
        # Verificar si la tercera línea no es "eula=true"
        if len(lineas) >= numero_linea and lineas[numero_linea - 1].strip() != "eula=true":
            # Ejecutar lo que necesites aquí si la tercera línea no es "eula=true"
            print("La tercera línea no es 'eula=true'. Ejecutando acción...")
            # Acción a ejecutar
            
            # Editar la tercera línea a "eula=true"
            lineas[numero_linea - 1] = nuevo_contenido + '\n'

            with open(ruta_completa, 'w') as archivo:
                archivo.writelines(lineas)
            print(f"Línea {numero_linea} editada correctamente.")
        
    except FileNotFoundError:
        print(f"No se encontró el archivo {ruta_completa}.")
        
    except Exception as e:
        print(f"Ocurrió un error al editar la línea: {e}")

# Funcion para descargar Java JDK 22 portable
def descargar_java_jdk_22():
    
    url_zip = "https://download.oracle.com/java/22/archive/jdk-22_windows-x64_bin.zip"
    nombre_archivo_zip = "jdk-22_windows-x64_bin.zip"
    ruta_destino = "Data/Java"
    javaw = "Data/Java/jdk-22/bin/javaw.exe"
    ruta_zip = os.path.join(ruta_destino, nombre_archivo_zip)
    # Comprobar si el archivo ya existe

    try:
        if not os.path.exists(ruta_destino):
            os.makedirs(ruta_destino)
        
        if not os.path.exists(ruta_zip):
            with requests.get(url_zip, stream=True) as respuesta:
                total_size = int(respuesta.headers.get('content-length', 0))
                chunk_size = 8192  # Tamaño del chunk
                received_bytes = 0

                with open(ruta_zip, 'wb') as archivo:
                    progress_bar = ctk.CTkProgressBar(window, orientation='horizontal', mode='determinate')
                    progress_bar.place(relx=0, rely=1, relwidth=1, anchor='sw')

                    for data in respuesta.iter_content(chunk_size=chunk_size):
                        received_bytes += len(data)
                        archivo.write(data)
                        if total_size > 0:
                            percent_complete = received_bytes / total_size * 100
                            # Actualizar la barra de progreso cada 5%
                            if percent_complete % 5 == 0:
                                print(f"Descargado: {percent_complete:.2f}%")
                                progress_bar.destroy()

        if not os.path.exists(javaw):
            # Descomprimir el archivo ZIP
            with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                zip_ref.extractall(ruta_destino)

            print(f"Descarga de '{nombre_archivo_zip}' completada en '{ruta_destino}'")
        else:
            print(f"'{nombre_archivo_zip}' ya existe en '{ruta_destino}', no es necesario descargarlo nuevamente.")
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")
 
# Funcion para guardar el archivo de texto que se esta modificando
def guardar_archivo(ruta_archivo, contenido):
    with open(ruta_archivo, 'w') as archivo:
        archivo.write(contenido) 

# Destruye el boton que se envie a la funcion
def destroy_servers_button(button):
    if button:
        button.destroy()



# Función para actualizar las barras de progreso para el uso de CPU y RAM
def update_progress_bars():
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    bar_cpu.set(cpu_percent / 100)
    bar_ram.set(ram_percent / 100)
    label_cpu.configure(text=f'CPU: {cpu_percent}%')
    label_ram.configure(text=f'RAM: {ram_percent}%')
    cpu_ram_frame.after(1000, update_progress_bars)

# Start updating progress bars
update_progress_bars()



window.mainloop()

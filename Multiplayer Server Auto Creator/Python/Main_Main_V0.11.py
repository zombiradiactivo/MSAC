import customtkinter as ctk
from random import choice
import tkinter as tk
from tkinter import ttk
import psutil
import os
import subprocess
import requests
import threading
import shutil
from py7zr import unpack_7zarchive 


# Window setup
window = ctk.CTk()
window.title('Server Creator')
window.geometry('800x400')

# Función para actualizar las barras de progreso para el uso de CPU y RAM
def update_progress_bars():
    #cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    #bar_cpu['value'] = cpu_percent
    bar_ram['value'] = ram_percent
    #label_cpu.configure(text=f'CPU: {cpu_percent}%')
    label_ram.configure(text=f'RAM: {ram_percent}%')
    cpu_ram_frame.after(1000, update_progress_bars)

# Crear el rectángulo de texto para ingresar comandos
#input_command_text = tk.Text(window, height=2, width=20)
#input_command_text.place(relx=0.5, rely=0.9, anchor='center')

# Ip setup
Ip_bar = ctk.CTkFrame(window)
Ip_bar.place(relx=0.05, rely=0, relwidth=0.2, relheight=0.1) #relwidth=0.2

#Funcion para coger la direccion ip publica 
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




# Configuración de la barra lateral
sidebar_panel = ctk.CTkFrame(window)
sidebar_panel.place(relx=0.05, rely=0.2, relwidth=0.2, relheight=0.5)

# Stopsidebar setup
sidebar_panel2 = ctk.CTkFrame(window)
sidebar_panel2.place(relx=0.75, rely=0, relwidth=0.2, relheight=0.1)

# Configuración del submenú
submenu_frame = ctk.CTkFrame(window)
submenu_frame.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)

# Configuración de pestañas
Tabview = ctk.CTkTabview(window)
Tabview.place(relx=0.65, rely=0.2, relwidth=0.3, relheight=0.5)


tab_1 = Tabview.add("Minecraft")










# Botones para la barra lateral
def servers_button():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='XAMPP', command=XAMPP_Installer).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Chat').pack(expand=True, fill='both', padx=5, pady=5)

def destroy_servers_button(button):
    if button:
        button.destroy()



def games_button():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Minecraft', command=Minecraft_Loader).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Satisfactory').pack(expand=True, fill='both', padx=5, pady=5)

ctk.CTkButton(sidebar_panel, text='Servers', command=servers_button).pack(expand=True, fill='both', padx=5, pady=5)
ctk.CTkButton(sidebar_panel, text='Games', command=games_button).pack(expand=True, fill='both', padx=5, pady=5)


# Submenú de funciones de servidores
 
def Xampp_Menu():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    global Button_Apache
    Button_Apache = ctk.CTkButton(submenu_frame, text='Apache', command=Apache_Start)
    Button_Apache.pack(expand=True, fill='both', padx=5, pady=5)
    global Button_Filezilla
    Button_Filezilla = ctk.CTkButton(submenu_frame, text='Filezilla')
    Button_Filezilla.pack(expand=True, fill='both', padx=5, pady=5)

def XAMPP_Installer():
    url_archivo = 'https://netcologne.dl.sourceforge.net/project/xampp/XAMPP%20Windows/8.2.12/xampp-windows-x64-8.2.12-0-VS16-installer.exe'
    nombre_local = 'XAMPP.exe'
    ruta_carpeta_descarga = 'temp/xampp'
    ruta_instalador = 'temp/xampp/xampp.exe'
    ruta_carpeta_temp = 'temp'
    ruta_archivo_indicador = 'C:/xampp/xampp-control.exe'

    def verificar_xampp_instalado():
        return os.path.exists(ruta_archivo_indicador)

    def descargar_instalar_xampp():
        # Crear un hilo para la descarga del archivo
        descarga_thread = threading.Thread(target=instalar_xampp)
        descarga_thread.start()
    
    def instalar_xampp():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta_descarga)
        # Comando para ejecutar el instalador
        cmd = f'powershell.exe -Command "Start-Process \'{ruta_instalador}\' -Verb runAs"'
        subprocess.run(cmd, shell=True)

    # Llamada a la función
    xampp_instalado = verificar_xampp_instalado()  
    

    # Puedes usar la variable xampp_instalado para tomar decisiones en tu aplicación
    if xampp_instalado:
        # XAMPP está instalado, realiza alguna acción
        print("XAMPP está instalado.")
        Xampp_Menu()  # Llamada a la función Xampp_Menu
    else:
        # XAMPP no está instalado, realiza alguna otra acción
        print("XAMPP no está instalado.")
        descargar_instalar_xampp()
        #borrar_carpeta(ruta_carpeta_temp)

def Apache_Start():
    Apache_Start_Exe = 'C:/xampp/apache/bin/httpd.exe'
    Button_Stop_Apache = ctk.CTkButton(sidebar_panel2, text='Stop Apache', command=lambda: (Apache_Stop(process, Button_Stop_Apache)))
    Button_Stop_Apache.pack(expand=True, fill='both', padx=5, pady=5)
    cmd = f'powershell.exe Start-Process "{Apache_Start_Exe}"'  # Start Apache server
    process = subprocess.Popen(cmd, shell=False)
    
    Button_Apache.configure(state="disabled")
    
   # Espera a que se inicie el servidor Apache
    process.wait()

def Apache_Stop(process, button):
    if button:
        button.destroy()
    # Obtiene una lista de todos los procesos en ejecución
    processes = psutil.process_iter()
    
    Button_Apache.configure(state="enabled")
    
    # Procesa la lista de procesos
    for process in processes:
        # Comprueba si el proceso tiene el nombre "httpd.exe"
        if process.name() == "httpd.exe":
            # Finaliza el proceso
            process.kill()


def Filezilla_Start():
    Filezilla_Start_Exe = 'C:/xampp/FileZillaFTP/FileZillaServer.exe'
    Button_Stop_Filezilla = ctk.CTkButton(sidebar_panel2, text='Stop Filezilla', command=lambda: (Filezilla_Stop(process, Button_Stop_Filezilla)))
    Button_Stop_Filezilla.pack(expand=True, fill='both', padx=5, pady=5)
    cmd = f'powershell.exe Start-Process "{Filezilla_Start_Exe}"'  
    process = subprocess.Popen(cmd, shell=False)
    
    Button_Filezilla.configure(state="disabled")
    
    process.wait()

def Filezilla_Stop(process, button):
    if button:
        button.destroy()
    processes = psutil.process_iter()
    
    Button_Filezilla.configure(state="enabled")
    
    for process in processes:

        if process.name() == "FileZillaServer.exe":
            process.kill()


# Submenú de funciones de juegos 
def Minecraft_Loader():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Minecraft Vanilla', command=Minecraft_Vanilla).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Minecraft Forge',   command=Minecraft_Forge).pack(expand=True, fill='both', padx=5, pady=5)


def Minecraft_Vanilla():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='1.20.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.19.4', command=descargar_1_19_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.18.2', command=descargar_1_18_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Vanilla_2).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_2():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Vanilla).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.17.1', command=descargar_1_17_1).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.16.5', command=descargar_1_16_5).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.15.2', command=descargar_1_15_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Vanilla_3).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_3():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Vanilla_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.14.4', command=descargar_1_14_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.13.2', command=descargar_1_13_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.12.2', command=descargar_1_12_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Vanilla_4).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_4():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Vanilla_3).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.11',  command=descargar_1_11_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.10',  command=descargar_1_10_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.9',   command=descargar_1_9_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Vanilla_5).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_5():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Vanilla_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.8.9',  command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.7.10',  command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.9',   command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)



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





def Minecraft_Forge():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='1.20.1', command=descargar_forge_1_20_1).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.19.4', command=descargar_forge_1_19_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.18.2', command=descargar_forge_1_18_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Forge_2).pack(expand=True, fill='both', padx=5, pady=5)
    
def Minecraft_Forge_2():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Forge).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.17.1', command=descargar_forge_1_17_1).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.16.5', command=descargar_forge_1_16_5).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.15.2', command=descargar_forge_1_15_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Forge_3).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_3():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Forge_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.14.4', command=descargar_forge_1_14_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.13.2', command=descargar_forge_1_13_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.12.2', command=descargar_forge_1_12_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Forge_4).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_4():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Forge_3).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.11.2', command=descargar_forge_1_11_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.10.2', command=descargar_forge_1_10_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.9.4',  command=descargar_forge_1_9_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Forge_5).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_5():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Forge_4).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.8',    command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.7',    command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.6',    command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older',  command=Minecraft_Forge_6).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_6():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Botones para submenú
    ctk.CTkButton(submenu_frame, text='Newer',  command=Minecraft_Forge_5).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.5', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.4', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.3', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)




#java -jar forge.jar --installServer

def descargar_forge_1_20_1():

    ruta_carpeta = 'Main/MCForge/1.20.1'
    nombre_local = "forge_1.20.1.jar"
    type = "modded"
    category = "forge"
    version = "1.20.1"
    ejecutable_modificado = "@user_jvm_args.txt @libraries/net/minecraftforge/forge/1.20.1-47.2.30/win_args.txt %*"
    ejecutable = "run.bat"
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
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
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
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
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
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
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_16_5():

    ruta_carpeta = 'Main/MCForge/1.16.5'
    nombre_local = "forge_1.16.5.jar"
    type = "modded"
    category = "forge"
    version = "1.16.5"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = ""
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_15_2():

    ruta_carpeta = 'Main/MCForge/1.15.2'
    nombre_local = "forge_1.15.2.jar"
    type = "modded"
    category = "forge"
    version = "1.15.2"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = f"-jar {ejecutable} -Xmx4G -Xms4G"
    java_JDK_22 = "C:\\Program Files\\Java\\jdk-22\\bin\\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_14_4():

    ruta_carpeta = 'Main/MCForge/1.14.4'
    nombre_local = "forge_1.14.4.jar"
    type = "modded"
    category = "forge"
    version = "1.14.4"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = ""
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_13_2():

    ruta_carpeta = 'Main/MCForge/1.13.2'
    nombre_local = "forge_1.13.2.jar"
    type = "modded"
    category = "forge"
    version = "1.13.2"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = ""
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_12_2():

    ruta_carpeta = 'Main/MCForge/1.12.2'
    nombre_local = "forge_1.12.2.jar"
    type = "modded"
    category = "forge"
    version = "1.12.2"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = ""
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_11_2():

    ruta_carpeta = 'Main/MCForge/1.11.2'
    nombre_local = "forge_1.11.2.jar"
    type = "modded"
    category = "forge"
    version = "1.11.2"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = ""
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_10_2():

    ruta_carpeta = 'Main/MCForge/1.10.2'
    nombre_local = "forge_1.10.2.jar"
    type = "modded"
    category = "forge"
    version = "1.10.2"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = ""
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()

def descargar_forge_1_9_4():

    ruta_carpeta = 'Main/MCForge/1.9.4'
    nombre_local = "forge_1.9.4.jar"
    type = "modded"
    category = "forge"
    version = "1.9.4"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = ""
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()


def descargar_forge_1_00_0():

    ruta_carpeta = 'Main/MCForge/1.00.0'
    nombre_local = "forge_1.00.0.jar"
    type = "modded"
    category = "forge"
    version = "1.00.0"
    ejecutable = f"minecraft_server.{version}.jar"
    ejecutable_modificado = " @user_jvm_args.txt @libraries/net/minecraftforge/forge/1.00.0-45.2.15/win_args.txt %*"
    java_JDK_22 = "C:\Program Files\Java\jdk-22\bin\javaw.exe"
    def descargar_ejecutar():
        download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version)    
    threading.Thread(target=descargar_ejecutar).start()















# CPU and RAM progress bars setup
cpu_ram_frame = ctk.CTkFrame(window)
cpu_ram_frame.place(relx=0.75, rely=0.8, relwidth=0.2, relheight=0.1)

style = ttk.Style()
style.theme_use('clam') 

#bar_cpu = ctk.CTkProgressBar(cpu_ram_frame, orientation='horizontal', mode='determinate')
#bar_cpu.pack(expand=True, fill='both', padx=5, pady=5)

#label_cpu = ctk.CTkLabel(cpu_ram_frame)
#label_cpu.pack()

bar_ram = ctk.CTkProgressBar(cpu_ram_frame, orientation='horizontal', mode='determinate')
bar_ram.pack(expand=True, fill='both', padx=5, pady=5)

label_ram = ctk.CTkLabel(cpu_ram_frame)
label_ram.pack()



#Funcion para descargar un archivo 
def descargar_archivo(url, nombre_archivo, carpeta):
    try:
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        ruta_completa = os.path.join(carpeta, nombre_archivo)
        
        if not os.path.exists(ruta_completa):
            respuesta = requests.get(url, stream=True)
            total_size = int(respuesta.headers.get('content-length', 0))

            with open(ruta_completa, 'wb') as archivo:
                progress_bar = ctk.CTkProgressBar(window, orientation='horizontal', mode='determinate')
                progress_bar.place(relx=0, rely=1, relwidth=1, anchor='sw')


                received_bytes = 0
                for data in respuesta.iter_content(chunk_size=1024):
                    received_bytes += len(data)
                    archivo.write(data)
                    progress_bar['value'] = (received_bytes / total_size) * 100
                    window.update_idletasks()
                    
            print(f"Descarga de '{nombre_archivo}' completada en '{carpeta}'")
            progress_bar.destroy()
        else:
            print(f"'{nombre_archivo}' ya existe en '{carpeta}', no es necesario descargarlo nuevamente.")
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")


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

                with open(ruta_completa, 'wb') as archivo:
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
                                
        
            print(f"Descarga de '{nombre_archivo}' completada en '{carpeta}'")
        else:
            print(f"'{nombre_archivo}' ya existe en '{carpeta}', no es necesario descargarlo nuevamente.")
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")


# Ejecuta un archivo .jar en una carpeta 
def ejecutar_jar(ruta_carpeta, nombre_local):
        try:
            # Obtener la ruta absoluta al archivo .jar
            ruta_absoluta = os.path.abspath(os.path.join(ruta_carpeta))

            # Comando para ejecutar el archivo .jar usando Java
            comando = f"java -Xmx2048M -Xms2048M -jar {nombre_local}"

            # Ejecutar el archivo .jar
            subprocess.run(comando, shell=True, cwd=ruta_absoluta)
        except Exception as e:
            print(f"Error al ejecutar el archivo .jar: {e} {ruta_absoluta}")



# Decide si descargar, instalar o ejecutar el servidor forge dependiendo de los contenidos de la carpeta
def download_install_run_forge(ruta_carpeta, nombre_local, ejecutable, ejecutable_modificado, java_JDK_22, type, category, version):
    try:
        # Verificar si el archivo .jar ya está descargado
        ruta_absoluta = os.path.abspath(os.path.join(ruta_carpeta, nombre_local))
        print (ruta_absoluta)
        if not os.path.exists(ruta_absoluta):
            print("Descargando servidor Forge...")
            API_SERVERJARS_descargar_jar(type, category, version, ruta_carpeta)

        # Verificar si el servidor ya está instalado

        ruta_ejecutable = os.path.abspath(os.path.join(ruta_carpeta, ejecutable))
        print(ruta_ejecutable)
        if not os.path.exists(ruta_ejecutable):
            print("Instalando servidor Forge...")
            install_forge(ruta_carpeta, nombre_local)
            first_run_forge(ruta_carpeta)
            editar_eula(ruta_carpeta)

        # Ejecutar el servidor
        print("Ejecutando servidor Forge...")
        subprocess.run(f'"{java_JDK_22}" {ejecutable_modificado}', shell=True, cwd=ruta_carpeta)

    except Exception as e:
        print(f"Error al gestionar el servidor Forge: {e}")



# Instalar el servidor forge en una carpeta 
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


def first_run_forge(ruta_carpeta, version):
    nombre_eula = 'eula.txt'
    ruta_completa = os.path.join(ruta_carpeta, nombre_eula)
    try:
        if not os.path.exists(ruta_completa):
            print("El archivo Eula no existe")
            subprocess.run(f"minecraft_server.{version}.jar", shell=True, cwd=ruta_carpeta)
    except Exception as e:
        print(f"Error al gestionar el servidor Forge: {e}")

def borrar_carpeta(ruta_carpeta):
    try:
        # Borra la carpeta y su contenido de manera recursiva
        shutil.rmtree(ruta_carpeta)
        print(f"Carpeta '{ruta_carpeta}' y su contenido han sido eliminados correctamente.")
    except OSError as e:
        print(f"Error al borrar la carpeta '{ruta_carpeta}': {e}")


# Edita una linea especifica de un archivo a otra linea 
def editar_eula(ruta_carpeta):
    nombre_eula = 'eula.txt'
    numero_linea = "3"
    nuevo_contenido = "eula=true"
    ruta_completa = os.path.join(ruta_carpeta, nombre_eula)
    try:
        with open(ruta_completa, 'r') as archivo:
            lineas = archivo.readlines()
        # Verificar si el número de línea es válido
        if 0 < numero_linea <= len(lineas):
            lineas[numero_linea - 1] = nuevo_contenido + '\n'

            with open(ruta_completa, 'w') as archivo:
                archivo.writelines(lineas)
            print(f"Línea {numero_linea} editada correctamente.")
        else:
            print(f"El número de línea {numero_linea} no es válido para este archivo.")
    except FileNotFoundError:
        print(f"No se encontró el archivo {ruta_completa}.")
    except Exception as e:
        print(f"Ocurrió un error al editar la línea: {e}")


#def ejecutar_comando(event=None):
#    comando = input_command_text.get("1.0", "end-1c")  # Obtener el texto del rectángulo de texto
#    if comando.strip():  # Verificar si el comando no está vacío
#        enviar_comando_al_jar(comando)
#    input_command_text.delete("1.0", "end")  # Borrar el texto del rectángulo de texto


# Función para enviar el comando al .jar
#def enviar_comando_al_jar(comando):
#    if proceso_jar:
#        proceso_jar.stdin.write((comando + '\n').encode())
#        proceso_jar.stdin.flush()


# Variable global para almacenar el proceso del .jar
#proceso_jar = None


# Configurar la ejecución del comando al presionar Enter
# input_command_text.bind("<Return>", ejecutar_comando)


# Start updating progress bars
update_progress_bars()


window.mainloop()

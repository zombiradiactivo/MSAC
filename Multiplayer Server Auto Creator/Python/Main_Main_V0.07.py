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

# Function to update progress bars for CPU and RAM usage
def update_progress_bars():
    cpu_percent = psutil.cpu_percent()
    ram_percent = psutil.virtual_memory().percent
    bar_cpu['value'] = cpu_percent
    bar_ram['value'] = ram_percent
    label_cpu.configure(text=f'CPU: {cpu_percent}%')
    label_ram.configure(text=f'RAM: {ram_percent}%')
    cpu_ram_frame.after(1000, update_progress_bars)

# Crear el rectángulo de texto para ingresar comandos
input_command_text = tk.Text(window, height=2, width=20)
input_command_text.place(relx=0.5, rely=0.9, anchor='center')

# Sidebar setup
sidebar_panel = ctk.CTkFrame(window)
sidebar_panel.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.5)

# Stopsidebar setup
sidebar_panel2 = ctk.CTkFrame(window)
sidebar_panel2.place(relx=0.75, rely=0, relwidth=0.2, relheight=0.1)

# Submenu setup
submenu_frame = ctk.CTkFrame(window)
submenu_frame.place(relx=0.35, rely=0.3, relwidth=0.3, relheight=0.5)

# Buttons for sidebar
def servers_button():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='XAMPP', command=XAMPP_Installer).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Chat').pack(expand=True, fill='both', padx=5, pady=5)

def stop_servers_button():
    for widget in sidebar_panel2.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(sidebar_panel2, text='XAMPP', command=XAMPP_Installer).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(sidebar_panel2, text='Chat').pack(expand=True, fill='both', padx=5, pady=5)

def games_button():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='Minecraft', command=Minecraft_Loader).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Satisfactory').pack(expand=True, fill='both', padx=5, pady=5)

ctk.CTkButton(sidebar_panel, text='Servers', command=servers_button).pack(expand=True, fill='both', padx=5, pady=5)
ctk.CTkButton(sidebar_panel, text='Games', command=games_button).pack(expand=True, fill='both', padx=5, pady=5)


# Submenu servers funtions
 
def Xampp_Menu():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='Apache', command=Apache_Start).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Filezilla').pack(expand=True, fill='both', padx=5, pady=5)

def XAMPP_Installer():
    url_archivo = 'https://netcologne.dl.sourceforge.net/project/xampp/XAMPP%20Windows/8.2.12/xampp-windows-x64-8.2.12-0-VS16-installer.exe'
    nombre_local = 'XAMPP.exe'
    ruta_carpeta_descarga = 'temp/xampp'
    ruta_instalador = 'temp/xampp/xampp.exe'
    ruta_carpeta_temp = 'temp'
    ruta_archivo_indicador = 'C:/xampp/xampp-control.exe'


    # Llamada a la función
    xampp_instalado = verificar_xampp_instalado()  


    def verificar_xampp_instalado():
        return os.path.exists(ruta_archivo_indicador)


    # Puedes usar la variable xampp_instalado para tomar decisiones en tu aplicación
    if xampp_instalado:
        # XAMPP está instalado, realiza alguna acción
        print("XAMPP está instalado.")
        Xampp_Menu()  # Llamada a la función Xampp_Menu
    else:
        # XAMPP no está instalado, realiza alguna otra acción
        print("XAMPP no está instalado.")
        instalar_xampp()
        # borrar_carpeta(ruta_carpeta_temp)
    

    def instalar_xampp():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta_descarga)
        # Comando para ejecutar el instalador
        cmd = f'powershell.exe Start-Process "{ruta_instalador}" --help -Verb runAs'  # reemplazar --help con --unattendedmodeui
        subprocess.run(cmd, shell=True)





def Apache_Start():
    Apache_Start_Bat = 'C:/xampp/apache_start.bat'
    ctk.CTkButton(sidebar_panel2, text='Stop Apache', command=Apache_Stop).pack(expand=True, fill='both', padx=5, pady=5)
    cmd = f'powershell.exe Start-Process "{Apache_Start_Bat}"'  
    process = subprocess.Popen(cmd, shell=True)
    return process

def Apache_Stop(process):
    # Aquí puedes detener el proceso usando terminate()
    process.terminate()
    # También podrías usar kill() en lugar de terminate() si es necesario
    # process.kill()



# Submenu de funciones de juegos
def Minecraft_Loader():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='Minecraft Vanilla', command=Minecraft_Vanilla).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Minecraft Forge', command=Minecraft_Forge).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.20.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.19.4', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.18.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Vanilla_2).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_2():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Vanilla).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.17.1', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.16.5', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.15.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Vanilla_3).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_3():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.14.4', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.13.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.12.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Vanilla_4).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_4():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.11', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.10', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.9', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Vanilla_5).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Vanilla_5():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.11', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.10', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.9', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)

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
    # Nuevo contenido que quieres escribir en esa línea
    nuevo_contenido = 'eula=true'
    def descargar_ejecutar():
        descargar_archivo(url_archivo, nombre_local, ruta_carpeta)
        ejecutar_jar(ruta_carpeta, nombre_local)
        editar_eula(ruta_completa_eula, numero_linea, nuevo_contenido)

    threading.Thread(target=descargar_ejecutar).start()




def Minecraft_Forge():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.20.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.19.4', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.18.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Forge_2).pack(expand=True, fill='both', padx=5, pady=5)
    
def Minecraft_Forge_2():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Vanilla).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.17.1', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.16.5', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.15.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Forge_3).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_3():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.14.4', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.13.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.12.2', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Forge_4).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_4():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.11', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.10', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.9', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Forge_5).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_5():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.11', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.10', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.9', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='Older', command=Minecraft_Forge_6).pack(expand=True, fill='both', padx=5, pady=5)

def Minecraft_Forge_6():
    for widget in submenu_frame.winfo_children():
        widget.destroy()
    # Buttons for submenu
    ctk.CTkButton(submenu_frame, text='1.8', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.7', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)
    ctk.CTkButton(submenu_frame, text='1.6', command=descargar_1_20_2).pack(expand=True, fill='both', padx=5, pady=5)



# CPU and RAM progress bars setup
cpu_ram_frame = ctk.CTkFrame(window)
cpu_ram_frame.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.8)

style = ttk.Style()
style.theme_use('clam')  # Choose the theme you prefer

bar_cpu = ttk.Progressbar(cpu_ram_frame, orient='horizontal', mode='determinate')
bar_cpu.pack(expand=True, fill='both', padx=5, pady=5)

label_cpu = ctk.CTkLabel(cpu_ram_frame)
label_cpu.pack()

bar_ram = ttk.Progressbar(cpu_ram_frame, orient='horizontal', mode='determinate')
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
                progress_bar = ttk.Progressbar(window, orient='horizontal', mode='determinate', style="Horizontal.TProgressbar")
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

#Funcion para borrar una carpeta
def borrar_carpeta(ruta_carpeta):
    try:
        # Borra la carpeta y su contenido de manera recursiva
        shutil.rmtree(ruta_carpeta)
        print(f"Carpeta '{ruta_carpeta}' y su contenido han sido eliminados correctamente.")
    except OSError as e:
        print(f"Error al borrar la carpeta '{ruta_carpeta}': {e}")


# Ejecuta un archivo .jar en una carpeta 
def ejecutar_jar( ruta_carpeta, nombre_local):
        try:
            # Obtener la ruta absoluta al archivo .jar
            ruta_absoluta = os.path.abspath(os.path.join(ruta_carpeta))

            # Comando para ejecutar el archivo .jar usando Java
            comando = f"java -Xmx2048M -Xms2048M -jar {nombre_local}"

            # Ejecutar el archivo .jar
            subprocess.run(comando, shell=True, cwd=ruta_absoluta)
        except Exception as e:
            print(f"Error al ejecutar el archivo .jar: {e} {ruta_absoluta}")


# Edita una linea especifica de un archivo a otra linea 
def editar_eula(ruta_completa, numero_linea, nuevo_contenido):
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


def ejecutar_comando(event=None):
    comando = input_command_text.get("1.0", "end-1c")  # Obtener el texto del rectángulo de texto
    if comando.strip():  # Verificar si el comando no está vacío
        enviar_comando_al_jar(comando)
    input_command_text.delete("1.0", "end")  # Borrar el texto del rectángulo de texto


# Función para enviar el comando al .jar
def enviar_comando_al_jar(comando):
    if proceso_jar:
        proceso_jar.stdin.write((comando + '\n').encode())
        proceso_jar.stdin.flush()


# Variable global para almacenar el proceso del .jar
proceso_jar = None


# Configurar la ejecución del comando al presionar Enter
input_command_text.bind("<Return>", ejecutar_comando)


# Start updating progress bars
update_progress_bars()

window.mainloop()
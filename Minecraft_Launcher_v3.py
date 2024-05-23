from tkinter import Tk, Label, Entry, Button, mainloop, ttk
from tkinter.ttk import Combobox
import minecraft_launcher_lib
import customtkinter as ctk
import subprocess
import hashlib
import json
import uuid
import sys
import os

window = ctk.CTk()
window.title("Minecraft Launcher")
window.geometry('320x240')
window.minsize(320, 240)

def generar_uuid_con_usuario_contrasena(username_input, password_input):
    # Concatenar el usuario y la contraseña
    datos_concatenados = f"{username_input}:{password_input}".encode('utf-8')

    # Aplicar una función de hash (SHA-256 en este caso) y obtener una cadena hexadecimal
    hashed_data_hex = hashlib.sha256(datos_concatenados).hexdigest()

    # Tomar una porción de 32 caracteres de la cadena hexadecimal para crear el UUID
    # (el UUID versión 4 requiere 32 dígitos hexadecimales)
    return str(uuid.UUID(hex=hashed_data_hex[:32], version=4))

def load_profiles():
    try:
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    except FileNotFoundError:
        profiles = []
    return profiles

def update_combobox(combobox, profiles):
    # Actualizar los valores del combobox con los perfiles cargados
    combobox_values = [f"{profile['username']} - {profile['version']} - {profile['jvmarguments']} - {profile['is_forge']}" for profile in profiles]
    combobox['values'] = combobox_values

def on_profile_selected(event):
    # Obtener el perfil seleccionado del combobox
    selected_profile = profile_combobox.get()
    username, version, jvmarguments, is_forge = selected_profile.split(' - ')
    # Actualizar los campos de entrada con los valores del perfil seleccionado
    username_input.delete(0, ctk.END)
    username_input.insert(0, username)
    version_select.set(version)
    jvm_input.delete(0, ctk.END)
    jvm_input.insert(0, jvmarguments)
    if is_forge == "1":
        forge_checkbox.select()
    else:
        forge_checkbox.deselect()


def cerrar_aplicacion():
    os._exit(0)

window.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

username_frame_label = ctk.CTkFrame(window, fg_color="transparent")
username_frame_label.place(relx=0, rely=0.0, relwidth=0.5, relheight=0.15)

username_frame_entry = ctk.CTkFrame(window, fg_color="transparent")
username_frame_entry.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=0.15)

password_frame_label = ctk.CTkFrame(window, fg_color="transparent")
password_frame_label.place(relx=0, rely=0.15, relwidth=0.5, relheight=0.15)

password_frame_entry = ctk.CTkFrame(window, fg_color="transparent")
password_frame_entry.place(relx=0.5, rely=0.15, relwidth=0.5, relheight=0.15)

profile_frame_label = ctk.CTkFrame(window, fg_color="transparent")
profile_frame_label.place(relx=0, rely=0.3, relwidth=0.5, relheight=0.15)

profile_frame_combobox = ctk.CTkFrame(window, fg_color="transparent")
profile_frame_combobox.place(relx=0.5, rely=0.3, relwidth=0.5, relheight=0.15)

version_frame_label = ctk.CTkFrame(window, fg_color="transparent")
version_frame_label.place(relx=0, rely=0.45, relwidth=0.4, relheight=0.15)

version_frame_checkbox = ctk.CTkFrame(window, fg_color="transparent")
version_frame_checkbox.place(relx=0.27, rely=0.47, relwidth=0.25, relheight=0.1)

version_frame_combobox = ctk.CTkFrame(window, fg_color="transparent")
version_frame_combobox.place(relx=0.5, rely=0.45, relwidth=0.5, relheight=0.15)

jvm_frame_label = ctk.CTkFrame(window, fg_color="transparent")
jvm_frame_label.place(relx=0, rely=0.6, relwidth=0.5, relheight=0.15)

jvm_frame_entry = ctk.CTkFrame(window, fg_color="transparent")
jvm_frame_entry.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.15)

save_profile_frame = ctk.CTkFrame(window, fg_color="transparent")
save_profile_frame.place(relx=0., rely=0.8, relwidth=0.5, relheight=0.20)

launch_frame = ctk.CTkFrame(window, fg_color="transparent")
launch_frame.place(relx=0.5, rely=0.8, relwidth=0.5, relheight=0.20)

ctk.CTkLabel(username_frame_label, text="Username:").pack(fill='both', expand=True, padx=5, pady=5)
username_input = ctk.CTkEntry(username_frame_entry)
username_input.pack(fill='both', expand=True, padx=5, pady=5)

ctk.CTkLabel(password_frame_label, text="Password:").pack(fill='both', expand=True, padx=5, pady=5)
password_input = ctk.CTkEntry(password_frame_entry)
password_input.pack(fill='both', expand=True, padx=5, pady=5)

forge_checkbox = ctk.CTkCheckBox(version_frame_checkbox, text="Forge")
forge_checkbox.pack(side='left', padx=5)

profiles = load_profiles()
ctk.CTkLabel(profile_frame_label, text="User Profile:").pack(fill='both', expand=True, padx=5, pady=5)
profile_combobox = Combobox(profile_frame_combobox)
profile_combobox.pack(fill='both', expand=True, padx=5, pady=5)
update_combobox(profile_combobox, profiles)
profile_combobox.bind("<<ComboboxSelected>>", on_profile_selected)

style = ttk.Style()
style.theme_use('clam')

minecraft_directory = 'minecraft'
versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
version_list = [i["id"] for i in versions]

ctk.CTkLabel(version_frame_label, text="Version:").pack(fill='both', expand=True, padx=5, pady=5)
version_select = Combobox(version_frame_combobox, values=version_list)
version_select.pack(fill='both', expand=True, padx=5, pady=5)
version_select.set(version_list[0] if version_list else "")

ctk.CTkLabel(jvm_frame_label, text="JVM Arguments:").pack(fill='both', expand=True, padx=5, pady=5)
jvm_input = ctk.CTkEntry(jvm_frame_entry)
jvm_input.pack(fill='both', expand=True, padx=5, pady=5)

def save_profile():
    # Obtener los valores de entrada del usuario y la versión seleccionada
    username = username_input.get()
    version = version_select.get()
    jvm_arguments = jvm_input.get()
    is_forge = forge_checkbox.get()
    profile = {"username": username, "version": version, "jvmarguments": jvm_arguments, "is_forge": is_forge}
    
    # Intentar cargar perfiles existentes, si el archivo no existe, inicializar una lista vacía
    try:
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    except FileNotFoundError:
        profiles = []

    # Agregar el nuevo perfil a la lista
    profiles.append(profile)

    # Guardar la lista actualizada de perfiles en el archivo JSON
    with open("profiles.json", "w") as file:
        json.dump(profiles, file, indent=4)

def install_forge(version):
    forge_version = "forge-" + version
    minecraft_launcher_lib.forge.install_forge_version(version, minecraft_directory, forge_version)

def launch():
    # Obtener los valores de entrada del usuario y la versión seleccionada
    username = username_input.get()
    version = version_select.get()
    jvm_arguments = jvm_input.get()

    if forge_checkbox.get():
        # Instalar Forge para la versión seleccionada
        install_forge(version)
    else:
        # Instalar la versión seleccionada de Minecraft
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory)

    # Configurar las opciones para el comando de lanzamiento de Minecraft
    options = {
        "username": username,
        "uuid": generar_uuid_con_usuario_contrasena(username, password_input.get()),
        "jvmArguments": jvm_arguments.split()  # Convertir los argumentos JVM en una lista
    }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)

    print(f"Este es tu uuid: {options['uuid']}")

    # Ejecutar el comando de lanzamiento de Minecraft
    subprocess.run(minecraft_command)
    
ctk.CTkButton(save_profile_frame, text="Save Profile", command=save_profile).pack(fill='both', expand=True, padx=5, pady=5)
ctk.CTkButton(launch_frame, text="Launch", command=launch).pack(fill='both', expand=True, padx=5, pady=5)

window.mainloop()

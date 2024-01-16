from tkinter import Tk, Label, Entry, Button, mainloop, ttk
from tkinter.ttk import Combobox
import minecraft_launcher_lib
import subprocess
import sys
import os
import pathlib
import uuid
import hashlib

def generar_uuid_con_usuario_contrasena(username_input, password_input):
    # Concatenar el usuario y la contraseña
    datos_concatenados = f"{username_input}:{password_input}".encode('utf-8')

    # Aplicar una función de hash (SHA-256 en este caso) y obtener una cadena hexadecimal
    hashed_data_hex = hashlib.sha256(datos_concatenados).hexdigest()

    # Tomar una porción de 32 caracteres de la cadena hexadecimal para crear el UUID
    # (el UUID versión 4 requiere 32 dígitos hexadecimales)
    return str(uuid.UUID(hex=hashed_data_hex[:32], version=4))


window = Tk()
window.title("Minecraft Launcher")

Label(window, text="Username:").grid(row=0, column=0)
username_input = Entry(window)
username_input.grid(row=0, column=1)

Label(window, text="Password:").grid(row=1, column=0)
password_input = Entry(window)
password_input.grid(row=1, column=1)

style = ttk.Style()
style.theme_use('clam')

minecraft_directory = 'minecraft'
versions = minecraft_launcher_lib.utils.get_available_versions(minecraft_directory)
version_list = []

for i in versions:
    version_list.append(i["id"])

Label(window, text="Version:").grid(row=2, column=0)
version_select = Combobox(window, values=version_list)
version_select.grid(row=2, column=1)
version_select.current(0)


def launch():
    window.withdraw()

    minecraft_launcher_lib.install.install_minecraft_version(version_select.get(), minecraft_directory)

    options = {
        "username": username_input.get(),  # Obtén el nombre de usuario desde el Entry
        "uuid": generar_uuid_con_usuario_contrasena(username_input.get(), password_input.get()),  # Genera el UUID con los datos ingresados
    }
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version_select.get(), minecraft_directory, options)

    print(f"Este es tu uuid: {options['uuid']}")

    subprocess.run(minecraft_command)

    sys.exit(0)


Button(window, text="Launch", command=launch).grid(row=4, column=1)

window.mainloop()
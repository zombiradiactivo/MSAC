import subprocess
import tkinter as tk
from tkinter import messagebox
import minecraft_launcher_lib


# Función para iniciar Minecraft con el nombre de usuario y la versión seleccionada
def iniciar_minecraft():
    nombre_usuario = entry_usuario.get()
    version = versiones_disponibles.get()

    if nombre_usuario.strip() == "":
        messagebox.showerror("Error", "Por favor, introduce un nombre de usuario.")
        return

    if version == "":
        messagebox.showerror("Error", "Por favor, selecciona una versión.")
        return

    try:
        subprocess.Popen(['java', '-jar', f'Minecraft_{version}.jar', f'--username={nombre_usuario}'])
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo Minecraft_{version}.jar")

# Crear la ventana principal
root = tk.Tk()
root.title("Launcher de Minecraft")

# Etiqueta y campo de entrada para el nombre de usuario
label_usuario = tk.Label(root, text="Nombre de Usuario:")
label_usuario.pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

# Etiqueta y lista desplegable para seleccionar la versión
label_version = tk.Label(root, text="Selecciona la versión:")
label_version.pack()
versiones_disponibles = tk.StringVar(root)
versiones_disponibles.set("") # Valor inicial
opciones_versiones = ["1.17.1", "1.16.5", "1.15.2"]  # Puedes agregar más versiones aquí
menu_versiones = tk.OptionMenu(root, versiones_disponibles, *opciones_versiones)
menu_versiones.pack()

# Botón para iniciar Minecraft
boton_iniciar = tk.Button(root, text="Iniciar Minecraft", command=iniciar_minecraft)
boton_iniciar.pack()

# Ejecutar el bucle principal de la interfaz gráfica
root.mainloop()

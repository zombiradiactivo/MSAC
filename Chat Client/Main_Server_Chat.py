import os
import socket
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox



class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('250x150')
        self.minsize(250, 150)

        # Configuración del submenú
        self.frame = ctk.CTkFrame(self)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.HOST = '127.0.0.1'
        self.PORT = 5555
        self.Button_Chat_Server = None

        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        # Terminar el proceso de Python
        os._exit(0)

    def Chat_Menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Botones para submenú
        self.entry_label_chat = ctk.CTkLabel(self.frame, text="Seleccionar puerto 0 a 65535 ", fg_color="transparent")
        self.entry_label_chat.pack(expand=False, fill='both')
        self.entry_label_chat1 = ctk.CTkLabel(self.frame, text="Puerto default 5555", fg_color="transparent")
        self.entry_label_chat1.pack(expand=False, fill='both')
        self.entry_puerto_chat = ctk.CTkEntry(self.frame, validate="key", validatecommand=(self.register(self.validar_entrada), "%P"))
        self.entry_puerto_chat.pack(expand=False, fill='both', padx=5, pady=5)
        self.entry_puerto_chat.insert(index=5555,string=5555)

        if self.Button_Chat_Server is None:
            self.Button_Chat_Server = ctk.CTkButton(self.frame, text='Iniciar Server', command=self.Iniciar_Chat_Server)
            self.Button_Chat_Server.pack(expand=True, fill='both', padx=5, pady=5)

    def validar_entrada(self, entrada):
        try:
            valor = int(entrada)
            if valor < 0 or valor > 65535:
                return False
            # Verificar si el puerto ya está en uso
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('localhost', valor))
                except OSError:
                    messagebox.showerror("Error", f"El puerto {valor} ya está en uso.")
                    return False
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número válido.")
            return False
        return True

    def Iniciar_Chat_Server(self):
        # Verificar si se ha ingresado un puerto válido
        if self.validar_entrada(self.entry_puerto_chat.get()):
            self.PORT = int(self.entry_puerto_chat.get())
        else:
            self.PORT = 5555  # Usar el puerto predeterminado

        # Iniciar el servidor de chat con el puerto seleccionado
        self.server_thread = threading.Thread(target=self.handle_client)
        self.server_thread.start()


    def handle_client(self):
                                            
        # Configuración del servidor
        # Crear un socket TCP/IP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincular el socket a la dirección y puerto especificados
        server_socket.bind((self.HOST, self.PORT))

        # Escuchar conexiones entrantes
        server_socket.listen(5)
        print(f"Servidor de chat está escuchando en {self.HOST}:{self.PORT}")

        # Lista para almacenar los sockets de los clientes
        self.clients = []

        while True:
            # Esperar a una nueva conexión
            client_socket, address = server_socket.accept()

            # Agregar el socket del cliente a la lista
            self.clients.append(client_socket)

            # Iniciar un proceso para manejar la conexión con el cliente
            client_thread = threading.Thread(target=self.handle_client_thread, args=(client_socket, address))
            client_thread.start()



    def handle_client_thread(self, client_socket, address):
        def broadcast(message):
            for client in self.clients:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    self.clients.remove(client)
        print(f"Conexión establecida desde {address}")

        # Recibir y establecer el nombre de usuario del cliente
        username = client_socket.recv(1024).decode("utf-8")
        print(f"Nombre de usuario establecido para {address}: {username}")

        # Tu código para manejar la conexión con el cliente
        while True:
            # Esperar a recibir datos del cliente
            try:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break
                print(f"Mensaje recibido de {username}: {data}")

                # Reenviar el mensaje a todos los clientes conectados
                broadcast(f"{username}: {data}")
            except ConnectionResetError:
                break

        # Cerrar la conexión con el cliente
        print(f"Conexión cerrada con {username}")
        client_socket.close()
        broadcast(f"{username} -- Usuario desconectado ")

    def Stop_Chat_Server(self, button):
        if button:
            button.destroy()
        if self.Button_Chat_Server:
            self.Button_Chat_Server.configure(state="enabled")

app = ChatApp()
app.Chat_Menu()
app.mainloop()
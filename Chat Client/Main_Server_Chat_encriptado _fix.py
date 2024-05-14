import os
import socket
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode


class ChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('250x200')
        self.minsize(250, 200)

        # Configuración del submenú
        self.frame = ctk.CTkFrame(self)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.HOST = '127.0.0.1'
        self.PORT = '5555'
        self.Button_Chat_Server = None
        self.key = b'1234567890123456'  # Define la clave aquí
        self.iv = b'0000000000000000'  # Vector de inicialización (IV)
        
        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)


    def cerrar_aplicacion(self):
        # Terminar el proceso de Python
        os._exit(0)

    def Chat_Menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        # Botones de la interfaz
        self.key_label = ctk.CTkLabel(self.frame, text="Clave:")
        self.key_label.pack(expand=False, fill='both')

        self.key_entry = ctk.CTkEntry(self.frame, validate="key", validatecommand=(self.register(self.validar_key), "%P"))
        self.key_entry.pack(expand=False, fill='both', padx=0, pady=0)
        self.key_entry.insert(index=0, string=self.key)

        self.entry_label_chat = ctk.CTkLabel(self.frame, text="Seleccionar puerto 0 a 65535 ", fg_color="transparent")
        self.entry_label_chat.pack(expand=False, fill='both')

        self.entry_puerto_chat = ctk.CTkEntry(self.frame, validate="key", validatecommand=(self.register(self.validar_entrada), "%P"))
        self.entry_puerto_chat.pack(expand=False, fill='both', padx=5, pady=5)
        self.entry_puerto_chat.insert(index=0, string=self.PORT)

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
            print("Error", "Debe ingresar un número válido.")
            return False
        return True

    def validar_key(self, entrada):
        try:
            valor = int(entrada)
            if valor < 0 or valor > 9999999999999999:
                return False
        except ValueError:
            print("Error", "Debe ingresar un número válido.")
            return False
        return True

    def Iniciar_Chat_Server(self):
        if self.validar_entrada(self.entry_puerto_chat.get()):
            self.PORT = int(self.entry_puerto_chat.get())
        else:
            self.PORT = 5555  # Usar el puerto predeterminado
    
        # Obtener la clave ingresada por el usuario
        self.key = self.key_entry.get().encode("utf-8")
    
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
                    client.send(self.encrypt_message(message))  # Envía el mensaje encriptado
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
                encrypted_message = client_socket.recv(1024)
                if encrypted_message:
                    decrypted_message = self.decrypt_message(encrypted_message)  # Desencripta el mensaje recibido
                    print(f"Mensaje recibido de {username}: {decrypted_message}")
                    broadcast(f"{username}: {decrypted_message}")
            except ConnectionResetError:
                break

        # Cerrar la conexión con el cliente
        print(f"Conexión cerrada con {username}")
        client_socket.close()
        broadcast(f"{username} -- Usuario desconectado ")    
    
    def encrypt_message(self, message):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(message.encode()) + encryptor.finalize()
        return b64encode(ct)

    def decrypt_message(self, encrypted_message):
        try:
            cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
            decryptor = cipher.decryptor()
            pt = decryptor.update(b64decode(encrypted_message)) + decryptor.finalize()
            return pt.decode('utf-8', 'replace')  # Reemplazar los caracteres desconocidos por un carácter de reemplazo
        except UnicodeDecodeError:
            # Manejar el error de decodificación
            return "Error: No se pudo decodificar el mensaje"


app = ChatApp()
app.Chat_Menu()
app.mainloop()
import os
import socket
import threading
import tkinter as tk
import customtkinter as ctk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Cliente")

        self.username = "Usuario"
        self.server_ip = "127.0.0.1"
        self.server_port = 5555

        # Clave predeterminada
        self.key = b'1234567890123456'

        self.create_frames()  
        self.create_widgets()
     

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Clave para encriptación
        self.iv = b'0000000000000000'  # Vector de inicialización (IV)
        
        root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)
    def cerrar_aplicacion(self):
        # Terminar el proceso de Python
        os._exit(0)

    def create_frames(self):
        
        "transparent"
        self.username_frame_label = ctk.CTkFrame(self.root, fg_color="transparent")
        self.username_frame_label.place(relx=0, rely=0, relwidth=0.5, relheight=0.1)

        self.username_frame_entry = ctk.CTkFrame(self.root, fg_color="transparent")
        self.username_frame_entry.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1)

        self.key_frame_label = ctk.CTkFrame(self.root, fg_color="transparent")
        self.key_frame_label.place(relx=0, rely=0.07, relwidth=0.5, relheight=0.1)

        self.key_frame_entry = ctk.CTkFrame(self.root, fg_color="transparent")
        self.key_frame_entry.place(relx=0.5, rely=0.07, relwidth=0.5, relheight=0.1)

        self.server_frame_label = ctk.CTkFrame(self.root, fg_color="transparent")
        self.server_frame_label.place(relx=0, rely=0.14, relwidth=0.5, relheight=0.1)

        self.server_frame_entry = ctk.CTkFrame(self.root, fg_color="transparent")
        self.server_frame_entry.place(relx=0.5, rely=0.14, relwidth=0.5, relheight=0.1)

        self.port_frame_label = ctk.CTkFrame(self.root, fg_color="transparent")
        self.port_frame_label.place(relx=0, rely=0.21, relwidth=0.5, relheight=0.1)

        self.port_frame_entry = ctk.CTkFrame(self.root, fg_color="transparent")
        self.port_frame_entry.place(relx=0.5, rely=0.21, relwidth=0.5, relheight=0.1)

        self.connect_button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.connect_button_frame.place(relx=0, rely=0.28, relwidth=0.5, relheight=0.1)

        self.disconnect_button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.disconnect_button_frame.place(relx=0.5, rely=0.28, relwidth=0.5, relheight=0.1)

        self.messages_text_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.messages_text_frame.place(relx=0.01, rely=0.35, relwidth=0.98, relheight=0.55)

        self.message_entry_frame_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.message_entry_frame_frame.place(relx=0, rely=0.94, relwidth=0.8, relheight=0.1)

        self.send_button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.send_button_frame.place(relx=0.8, rely=0.94, relwidth=0.2, relheight=0.1)


    def create_widgets(self):


        self.username_label = ctk.CTkLabel(self.username_frame_label, text="Nombre de Usuario:")
        self.username_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.username_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.username_entry = ctk.CTkEntry(self.username_frame_entry)
        self.username_entry.place(relx=0.4, rely=0.2, relwidth=0.3, relheight=0.5)
        self.username_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.username_entry.insert(0, self.username)

        self.key_label = ctk.CTkLabel(self.key_frame_label, text="Clave:")
        self.key_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.key_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.key_entry = ctk.CTkEntry(self.key_frame_entry)
        self.key_entry.place(relx=0.4, rely=0.2, relwidth=0.3, relheight=0.5)
        self.key_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.key_entry.insert(0, self.key)

        self.server_label = ctk.CTkLabel(self.server_frame_label, text="IP del Servidor:")
        self.server_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.server_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.server_entry = ctk.CTkEntry(self.server_frame_entry)
        self.server_entry.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.server_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.server_entry.insert(0, self.server_ip)

        self.port_label = ctk.CTkLabel(self.port_frame_label, text="Puerto del Servidor:")
        self.port_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.port_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.port_entry = ctk.CTkEntry(self.port_frame_entry)
        self.port_entry.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.port_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.port_entry.insert(0, str(self.server_port))

        self.connect_button = ctk.CTkButton(self.connect_button_frame, text="Conectar", command=self.connect_to_server)
        self.connect_button.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.connect_button.pack(expand=False, fill='both', padx=5, pady=5)

        self.disconnect_button = ctk.CTkButton(self.disconnect_button_frame, text="Desconectar", command=self.disconnect_from_server)
        self.disconnect_button.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.disconnect_button.pack(expand=False, fill='both', padx=5, pady=5)


        self.messages_text = ctk.CTkTextbox(self.messages_text_frame, width=50, height=20)
        self.messages_text.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.messages_text.pack(expand=True, fill='both', padx=5, pady=5)

        self.message_entry = ctk.CTkEntry(self.message_entry_frame_frame, width=40)
        self.message_entry.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.message_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(self.send_button_frame, text="Enviar", command=self.send_message)
        self.send_button.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.send_button.pack(expand=False, fill='both', padx=5, pady=5)

    def connect_to_server(self):
        # Obtiene los valores de los campos de entrada
        self.username = self.username_entry.get()
        self.server_ip = self.server_entry.get()
        self.server_port = int(self.port_entry.get())
        self.key = self.key_entry.get().encode("utf-8")  # Obtener la clave ingresada por el usuario y codificarla en utf-8

        try:
            # Deshabilita el botón de conectar y habilita el botón de desconectar
            self.connect_button.configure(state="disabled")
            self.disconnect_button.configure(state="enabled")

            # Crea un nuevo socket de cliente
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conecta el socket al servidor utilizando la IP y el puerto proporcionados
            self.client_socket.connect((self.server_ip, self.server_port))

            # Envía el nombre de usuario codificado en utf-8 al servidor
            self.client_socket.send(self.username.encode("utf-8"))

            # Muestra un mensaje de conexión exitosa en el área de texto de mensajes
            self.messages_text.insert(tk.END, "Conexión exitosa\n")
            self.messages_text.see(tk.END)

            # Inicia un nuevo hilo para recibir mensajes del servidor
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            # Si hay un error, reconfigura los botones de conectar y desconectar
            self.connect_button.configure(state="enabled")
            self.disconnect_button.configure(state="disabled")

            # Muestra un mensaje de error en el área de texto de mensajes
            self.messages_text.insert(tk.END, f"Conexión fallida: {e}\n")
            self.messages_text.see(tk.END)

    def disconnect_from_server(self):
        try:
            # Habilita el botón de conectar y deshabilita el botón de desconectar
            self.connect_button.configure(state="enabled")
            self.disconnect_button.configure(state="disabled")

            # Cierra el socket del cliente
            self.client_socket.close()

            # Muestra un mensaje de desconexión exitosa en el área de texto de mensajes
            self.messages_text.insert(tk.END, "Desconectado del servidor\n")
            self.messages_text.see(tk.END)
        except Exception as e:
            # Si hay un error, reconfigura los botones de conectar y desconectar
            self.connect_button.configure(state="enabled")
            self.disconnect_button.configure(state="disabled")

            # Muestra un mensaje de error en el área de texto de mensajes
            self.messages_text.insert(tk.END, f"Error al desconectarse del servidor: {e}\n")
            self.messages_text.see(tk.END)



    def receive_messages(self):
        while True:
            try:
                # Recibe mensajes encriptados del servidor con un tamaño máximo de 1024 bytes
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message:
                    # Divide el mensaje en el nombre de usuario y el texto encriptado
                    parts = encrypted_message.split(b':', 1)
                    if len(parts) == 2:
                        # Decodifica el nombre de usuario y obtiene el texto encriptado
                        username = parts[0].decode("utf-8")
                        encrypted_text = parts[1]

                        # Desencripta el mensaje
                        decrypted_message = self.decrypt_message(encrypted_text)

                        # Inserta el mensaje desencriptado en el área de texto de mensajes
                        self.messages_text.insert(tk.END, f"{username}: {decrypted_message}\n")
                        self.messages_text.see(tk.END)

                        # Imprime el usuario y el mensaje desencriptado en la consola
                        print(f"Usuario: {username}, Mensaje desencriptado: {decrypted_message}")
                    else:
                        # Imprime un mensaje no válido si el formato es incorrecto
                        print("Mensaje recibido no válido:", encrypted_message)
            except Exception as e:
                # Imprime el error en la consola si ocurre un problema al recibir el mensaje
                print("Error al recibir mensaje:", e)
                break

    def send_message(self):
        # Obtiene el mensaje del campo de entrada
        message = self.message_entry.get()
        if message:
            # Encripta el mensaje
            encrypted_message = self.encrypt_message(message)

            # Envía el mensaje encriptado al servidor
            self.client_socket.send(encrypted_message)

            # Borra el campo de entrada de mensaje
            self.message_entry.delete(0, tk.END)

    def encrypt_message(self, message):
        # Crea un objeto Cipher para la encriptación usando el algoritmo AES en modo CFB
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
        
        # Crea un objeto encryptor a partir del Cipher
        encryptor = cipher.encryptor()
        
        # Encripta el mensaje. Primero se codifica el mensaje en bytes, luego se encripta y se finaliza
        ct = encryptor.update(message.encode()) + encryptor.finalize()
        
        # Codifica el mensaje encriptado en base64 y lo devuelve
        return b64encode(ct)
    
    def decrypt_message(self, encrypted_message):
        try:
            # Crea un objeto Cipher para la desencriptación usando el algoritmo AES en modo CFB
            cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
            
            # Crea un objeto decryptor a partir del Cipher
            decryptor = cipher.decryptor()
            
            # Desencripta el mensaje. Primero se decodifica el mensaje encriptado en base64, luego se desencripta y se finaliza
            pt = decryptor.update(b64decode(encrypted_message)) + decryptor.finalize()
            
            # Decodifica el texto desencriptado en utf-8, reemplazando caracteres desconocidos por un carácter de reemplazo
            return pt.decode('utf-8', 'replace')
        except UnicodeDecodeError:
            # Si ocurre un error al decodificar, devuelve un mensaje de error
            return "Error: No se pudo decodificar el mensaje"


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry('600x700')
    root.minsize(400,500)
    client = ChatClient(root)
    root.mainloop()

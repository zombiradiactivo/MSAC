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
        self.username = self.username_entry.get()
        self.server_ip = self.server_entry.get()
        self.server_port = int(self.port_entry.get())
        self.key = self.key_entry.get().encode("utf-8")  # Obtener la clave ingresada por el usuario

        try:   
            self.connect_button.configure(state="disabled")
            self.disconnect_button.configure(state="enabled")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.send(self.username.encode("utf-8"))
            self.messages_text.insert(tk.END, "Conexion exitosa\n")
            self.messages_text.see(tk.END)
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            self.connect_button.configure(state="enabled")
            self.disconnect_button.configure(state="disabled")
            self.messages_text.insert(tk.END, f"Conexion Fallida: {e}\n")
            self.messages_text.see(tk.END)

    def disconnect_from_server(self):
        try:
            self.connect_button.configure(state="enabled")
            self.disconnect_button.configure(state="disabled")
            self.client_socket.close()
            self.messages_text.insert(tk.END, "Desconectado del servidor\n")
            self.messages_text.see(tk.END)
        except Exception as e:
            self.connect_button.configure(state="enabled")
            self.disconnect_button.configure(state="disabled")
            self.messages_text.insert(tk.END, f"Error al desconectarse del servidor: {e}\n")
            self.messages_text.see(tk.END)


    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message:
                    # Dividir el mensaje en usuario y mensaje encriptado
                    parts = encrypted_message.split(b':', 1)
                    if len(parts) == 2:
                        username = parts[0].decode("utf-8")
                        encrypted_text = parts[1]
                        decrypted_message = self.decrypt_message(encrypted_text)
                        self.messages_text.insert(tk.END, f"{username}: {decrypted_message}\n")
                        self.messages_text.see(tk.END)
                        print(f"Usuario: {username}, Mensaje desencriptado: {decrypted_message}")   #Debug
                        print(f"MENSAJE ENCRIPTADO RECIBIDO {encrypted_message}")       #Debug
                        print(f"MENSAJE DESENCRIPTADO RECIBIDO {decrypted_message}")    #Debug
                    else:
                        print("Mensaje recibido no válido:", encrypted_message)
            except Exception as e:
                print("Error al recibir mensaje:", e)
                break

    def send_message(self):
        message = self.message_entry.get()
        print(F"MENSAJE ENVIADO {message}")
        if message:
            encrypted_message = self.encrypt_message(message)
            print(F"MENSAJE ENCRIPTADO ENVIADO {encrypted_message}")    #Debug
            self.client_socket.send(encrypted_message)
            self.message_entry.delete(0, tk.END)

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
            print("error")  #Debug
            return "Error: No se pudo decodificar el mensaje"

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry('600x700')
    root.minsize(400,500)
    client = ChatClient(root)
    root.mainloop()

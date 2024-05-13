import socket
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
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

        self.create_widgets()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Clave para encriptación
        self.key = b'Sixteen byte key'  # Define la clave aquí
        self.iv = b'0000000000000000'  # Vector de inicialización (IV)

    def create_widgets(self):


        self.username_label = ctk.CTkLabel(self.root, text="Nombre de Usuario:")
        #self.username_label.grid(row=0, column=0, sticky=tk.W)
        self.username_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.username_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.username_entry = ctk.CTkEntry(self.root)
        #self.username_entry.grid(row=0, column=1)
        self.username_entry.place(relx=0.4, rely=0.2, relwidth=0.3, relheight=0.5)
        self.username_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.username_entry.insert(0, self.username)

        self.server_label = ctk.CTkLabel(self.root, text="IP del Servidor:")
        #self.server_label.grid(row=1, column=0, sticky=tk.W)
        self.server_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.server_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.server_entry = ctk.CTkEntry(self.root)
        #self.server_entry.grid(row=1, column=1)
        self.server_entry.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.server_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.server_entry.insert(0, self.server_ip)

        self.port_label = ctk.CTkLabel(self.root, text="Puerto del Servidor:")
        #self.port_label.grid(row=2, column=0, sticky=tk.W)
        self.port_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.port_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.port_entry = ctk.CTkEntry(self.root)
        #self.port_entry.grid(row=2, column=1)
        self.port_entry.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.port_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.port_entry.insert(0, str(self.server_port))

        self.connect_button = ctk.CTkButton(self.root, text="Conectar", command=self.connect_to_server)
        #self.connect_button.grid(row=3, columnspan=2)
        self.connect_button.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.connect_button.pack(expand=False, fill='both', padx=5, pady=5)

        self.messages_text = ctk.CTkTextbox(self.root, width=50, height=20)
        #self.messages_text.grid(row=4, columnspan=2)
        self.messages_text.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.messages_text.pack(expand=True, fill='both', padx=5, pady=5)

        self.message_entry = ctk.CTkEntry(self.root, width=40)
        #self.message_entry.grid(row=5, column=0)
        self.message_entry.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.message_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(self.root, text="Enviar", command=self.send_message)
        #self.send_button.grid(expand=True,row=5, column=1)
        self.send_button.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
        self.send_button.pack(expand=False, fill='both', padx=5, pady=5)

    def connect_to_server(self):
        self.username = self.username_entry.get()
        self.server_ip = self.server_entry.get()
        self.server_port = int(self.port_entry.get())

        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.send(self.username.encode("utf-8"))
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message:
                    decrypted_message = self.decrypt_message(encrypted_message)
                    self.messages_text.insert(tk.END, decrypted_message + "\n")  # Desencripta y muestra el mensaje
                    self.messages_text.see(tk.END)
            except:
                break
            
    def send_message(self):
        message = self.message_entry.get()
        if message:
            encrypted_message = self.encrypt_message(message)
            self.client_socket.send(encrypted_message)
            self.message_entry.delete(0, tk.END)

    def encrypt_message(self, message):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(message.encode()) + encryptor.finalize()
        return b64encode(ct)

    def decrypt_message(self, encrypted_message):
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()
        pt = decryptor.update(b64decode(encrypted_message)) + decryptor.finalize()
        return pt.decode()

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry('400x500')
    root.minsize(400,500)
    client = ChatClient(root)
    root.mainloop()

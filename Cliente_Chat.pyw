import os
import socket
import threading
import tkinter as tk
import customtkinter as ctk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
from tkinter import filedialog  

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Cliente")

        self.username = "Usuario"
        self.server_ip = "127.0.0.1"
        self.server_port = 5555

        self.key = b'1234567890123456'

        self.create_frames()
        self.create_widgets()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.iv = b'0000000000000000'

        root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        os._exit(0)

    def create_frames(self):
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

        self.share_button_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.share_button_frame.place(relx=0.6, rely=0.89, relwidth=0.2, relheight=0.05)

        self.list_files_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.list_files_frame.place(relx=0.8, rely=0.89, relwidth=0.2, relheight=0.05)

        self.progress_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.progress_frame.place(relx=0.01, rely=0.89, relwidth=0.59, relheight=0.05)

    def create_widgets(self):
        self.username_label = ctk.CTkLabel(self.username_frame_label, text="Nombre de Usuario:")
        self.username_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.username_entry = ctk.CTkEntry(self.username_frame_entry)
        self.username_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.username_entry.insert(0, self.username)

        self.key_label = ctk.CTkLabel(self.key_frame_label, text="Clave:")
        self.key_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.key_entry = ctk.CTkEntry(self.key_frame_entry)
        self.key_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.key_entry.insert(0, self.key)

        self.server_label = ctk.CTkLabel(self.server_frame_label, text="IP del Servidor:")
        self.server_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.server_entry = ctk.CTkEntry(self.server_frame_entry)
        self.server_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.server_entry.insert(0, self.server_ip)

        self.port_label = ctk.CTkLabel(self.port_frame_label, text="Puerto del Servidor:")
        self.port_label.pack(expand=False, fill='both', padx=5, pady=5)

        self.port_entry = ctk.CTkEntry(self.port_frame_entry)
        self.port_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.port_entry.insert(0, str(self.server_port))

        self.connect_button = ctk.CTkButton(self.connect_button_frame, text="Conectar", command=self.connect_to_server)
        self.connect_button.pack(expand=False, fill='both', padx=5, pady=5)

        self.disconnect_button = ctk.CTkButton(self.disconnect_button_frame, text="Desconectar", command=self.disconnect_from_server)
        self.disconnect_button.pack(expand=False, fill='both', padx=5, pady=5)

        self.messages_text = ctk.CTkTextbox(self.messages_text_frame, width=50, height=20)
        self.messages_text.pack(expand=True, fill='both', padx=5, pady=5)

        self.message_entry = ctk.CTkEntry(self.message_entry_frame_frame, width=40)
        self.message_entry.pack(expand=False, fill='both', padx=5, pady=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = ctk.CTkButton(self.send_button_frame, text="Enviar", command=self.send_message)
        self.send_button.pack(expand=False, fill='both', padx=5, pady=5)

        self.share_button = ctk.CTkButton(self.share_button_frame, text="Compartir", command=self.send_file_thread)
        self.share_button.pack(expand=False, fill='both', padx=5, pady=5)

        self.list_files_button = ctk.CTkButton(self.list_files_frame, text="Descargar", command=self.download_window_thread)
        self.list_files_button.pack(expand=False, fill='both', padx=5, pady=5)

    def connect_to_server(self):
        self.username = self.username_entry.get()
        self.server_ip = self.server_entry.get()
        self.server_port = int(self.port_entry.get())
        self.key = self.key_entry.get().encode("utf-8")

        try:
            self.connect_button.configure(state="disabled")
            self.disconnect_button.configure(state="enabled")

            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.send(self.username.encode("utf-8"))

            self.messages_text.insert(tk.END, "Conexión exitosa\n")
            self.messages_text.see(tk.END)

            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            self.connect_button.configure(state="enabled")
            self.disconnect_button.configure(state="disabled")
            self.messages_text.insert(tk.END, f"Conexión fallida: {e}\n")
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
                encrypted_message = self.client_socket.recv(2048)
                if encrypted_message.startswith(b'MESSAGE:'):
                    message = encrypted_message[len('MESSAGE:'):]
                    parts = message.split(b':', 2)
                    if len(parts) == 3:
                        username = parts[0].decode("utf-8").strip()
                        encrypted_text = parts[2].strip()
                        decrypted_message = self.decrypt_message(encrypted_text)
                        self.messages_text.insert(tk.END, f"{username}: {decrypted_message}\n")
                        self.messages_text.see(tk.END)
                        print(f"Usuario: {username}, Mensaje desencriptado: {decrypted_message}")
                    else:
                        print("Mensaje recibido no válido:", message)
                elif encrypted_message.startswith(b'SERVER_MESSAGE:'):
                    message = encrypted_message[len('SERVER_MESSAGE:'):]
                    parts = message.split(b':', 1)
                    if len(parts) == 1:
                        server_message = parts[0].strip()
                        self.messages_text.insert(tk.END, f"Servidor: {server_message}\n")
                        self.messages_text.see(tk.END)
                        print(f" Mensaje del servidor: {message}")
                    else:
                        print("Mensaje del SERVIDOR recibido no válido:", message)
                elif encrypted_message.startswith(b'FILES_LIST:'): 
                    file_list = encrypted_message[len('FILES_LIST:'):]
                    if file_list:
                        lista = file_list.decode().split(",")
                        self.update_file_list(lista)
                    else:
                        print("Lista recibida no valida:", encrypted_message)

                elif encrypted_message.startswith(b"REQUESTED_FILE:"):
                    parts = encrypted_message.split(b':', 2)
                    if len(parts) == 3:
                        file_name = parts[1]
                        file_size = int(parts[2])

                        # Crear y configurar la barra de progreso
                        self.progress_bar = ctk.CTkProgressBar(self.shared_files_window_progress_frame, orientation='horizontal', mode='determinate')
                        self.progress_bar.pack(side="left", padx=10)
                        self.progress_bar.set(0)

                        file_content = b""
                        remaining_bytes = file_size
                        received_size = 0
                        while remaining_bytes > 0:
                            chunk_size = 4096
                            if remaining_bytes < chunk_size:
                                chunk_size = remaining_bytes
                            chunk = self.client_socket.recv(chunk_size)
                            if not chunk:
                                break
                            file_content += chunk
                            remaining_bytes -= len(chunk)
                            received_size += len(chunk)
                            self.progress_bar.set(received_size / file_size)

                        os.makedirs("downloads", exist_ok=True)  # Corregido el directorio
                        file_path = os.path.join("downloads", file_name.decode())  # Decodificar el nombre del archivo

                        with open(file_path, "wb") as f:
                            f.write(file_content)

                        self.messages_text.insert('end', f"Archivo {file_name.decode()} recibido y guardado.\n")  # Decodificar el nombre del archivo
                        self.messages_text.see(tk.END)
                        self.progress_bar.destroy()

            except Exception as e:
                print("Error al recibir mensaje:", e)
                break
      

    def send_message(self):
        message = self.message_entry.get()
        if message:
            encrypted_message = self.encrypt_message(message)
            header = f"MESSAGE:{encrypted_message.decode('utf-8')}".encode('utf-8')
            self.client_socket.send(header)
            self.message_entry.delete(0, tk.END)


    def send_file_thread(self):
        threading.Thread(target=self.send_file).start()

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_size = os.path.getsize(file_path)
            if file_size > 500 * 1024 * 1024:
                self.messages_text.insert(tk.END, "Error: El archivo excede el tamaño máximo de 500 MB.\n")
                self.messages_text.see(tk.END)
                return
            try:
                with open(file_path, "rb") as file:
                    file_name = os.path.basename(file_path)
                    header = f"THIS_IS_A_FILE:{file_name}:{file_size}".encode('utf-8')
                    self.client_socket.send(header)

                    progress = ctk.CTkProgressBar(self.progress_frame, orientation='horizontal', mode='determinate')
                    progress.pack(expand=True, fill='both', padx=5, pady=5)
                    progress.set(0)
                    progress['maximum'] = file_size
                    chunk_size = 8192
                    sent_size = 0
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        self.client_socket.send(chunk)
                        sent_size += len(chunk)
                        progress.set(sent_size / file_size)
                        self.root.update_idletasks()

                    self.messages_text.insert(tk.END, f"Archivo {file_name} enviado\n")
                    self.messages_text.see(tk.END)
                    progress.destroy()
            except Exception as e:
                self.messages_text.insert(tk.END, f"Error al enviar archivo: {e}\n")
                self.messages_text.see(tk.END)


    def download_window_thread(self):
        threading.Thread(target=self.download_window).start()

    def download_window(self):
        self.shared_files_window = ctk.CTkToplevel()
        self.shared_files_window.title("Archivos Compartidos")
        self.shared_files_window.geometry('450x300')
        self.shared_files_window.minsize(450, 300)
        
        # Frame para la lista de archivos
        self.files_list_frame = ctk.CTkScrollableFrame(self.shared_files_window, fg_color="transparent")
        self.files_list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        

        self.shared_files_window_progress_frame = ctk.CTkFrame(self.shared_files_window, fg_color="transparent")
        self.shared_files_window_progress_frame.pack(fill='x', padx=10, pady=10)
        
        self.progress_label = ctk.CTkLabel(self.shared_files_window_progress_frame, text="Progreso de la descarga:")
        self.progress_label.pack(side="left")
        
        self.list_files()

    def list_files(self):
        try:
            self.client_socket.send(b"LIST_FILES")
            print("LIST REQUESTED")
        except Exception as e:
            self.messages_text.insert(tk.END, f"Error al solicitar lista de archivos: {e}\n")
            self.messages_text.see(tk.END)

    def update_file_list(self, file_list):
        # Limpiar los widgets anteriores
        for widget in self.files_list_frame.winfo_children():
            widget.destroy()
        
        # Crear un botón para cada archivo en la lista
        for file in file_list:
            button = ctk.CTkButton(self.files_list_frame, text=file, command=lambda f=file: self.download_this_file(f))
            button.pack(pady=5)


    def download_this_file(self, file_name):
        header = f"DOWNLOAD_THIS_FILE:{file_name}".encode('utf-8')
        self.client_socket.send(header)


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
            return pt.decode('utf-8', 'replace')
        except UnicodeDecodeError:
            return "Error: No se pudo decodificar el mensaje"

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry('600x700')
    root.minsize(400,500)
    client = ChatClient(root)
    root.mainloop()

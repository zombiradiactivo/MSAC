import os
import socket
import threading
from datetime import datetime

class ChatApp():
    def __init__(self):
        super().__init__()

        self.HOST = '0.0.0.0'
        self.PORT = 5555

        self.Iniciar_Chat_Server()

    def Iniciar_Chat_Server(self):
        self.PORT_ENTRY = (input("Ingrese el puerto del servidor: "))
        if self.PORT_ENTRY:
            self.PORT = int(self.PORT_ENTRY)
        else:
            self.PORT = 5555

        self.server_thread = threading.Thread(target=self.handle_client)
        self.server_thread.start()

    def handle_client(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.HOST, self.PORT))
        server_socket.listen(5)
        print(f"Servidor de chat está escuchando en {self.HOST}:{self.PORT}")

        self.clients = []

        while True:
            client_socket, address = server_socket.accept()
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client_thread, args=(client_socket, address))
            client_thread.start()

    def handle_client_thread(self, client_socket, address):
        def broadcast(message):
            for client in self.clients:
                try:
                    client.send(message.encode())
                except:
                    self.clients.remove(client)

        print(f"Conexión establecida desde {address}")

        username = client_socket.recv(1024).decode("utf-8")
        print(f"Nombre de usuario establecido para {address}: {username}")

        while True:
            try:
                header = client_socket.recv(2048).decode("utf-8")
                if header.startswith("THIS_IS_A_FILE:"):
                    parts = header.split(':', 2)
                    if len(parts) == 3:
                        file_name = parts[1]
                        file_size = int(parts[2])

                        if file_size > 500 * 1024 * 1024:
                            client_socket.send(b"Servidor: ERROR: File size exceeds the maximum limit of 500 MB.\n")
                            continue

                        file_content = b""
                        remaining_bytes = file_size
                        while remaining_bytes > 0:
                            chunk_size = 8192
                            if remaining_bytes < chunk_size:
                                chunk_size = remaining_bytes
                            chunk = client_socket.recv(chunk_size)
                            if not chunk:
                                break
                            file_content += chunk
                            remaining_bytes -= len(chunk)

                        timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
                        file_base, file_ext = os.path.splitext(file_name)
                        new_file_name = f"{file_base}_{timestamp}{file_ext}"

                        os.makedirs("uploads", exist_ok=True)
                        file_path = os.path.join("uploads", new_file_name)

                        with open(file_path, "wb") as f:
                            f.write(file_content)

                        print(f"Archivo {new_file_name} recibido y guardado.\n")
                        client_socket.send(f"SERVER_MESSAGE:Archivo {new_file_name} recibido y guardado.\n".encode())
                        broadcast(f"El usuario {username} ha compartido el archivo {new_file_name}")
                
                elif header == "LIST_FILES":
                    os.makedirs("uploads", exist_ok=True)
                    files = os.listdir("uploads")
                    files_list = ",".join(files)
                    header = f"FILES_LIST:{files_list}".encode()
                    client_socket.send(header)

                elif header.startswith("DOWNLOAD_THIS_FILE:"):
                    os.makedirs("uploads", exist_ok=True)
                    file_name = header.split(":", 1)[1]
                    file_path = os.path.join("uploads", file_name)
                    if os.path.exists(file_path):
                        self.send_file(client_socket, file_name)
                    else:
                        client_socket.send(b"ERROR: File not found.\n")
                        
                elif header.startswith("MESSAGE:"):
                    message = header
                    if message:
                        print(f"Mensaje recibido de {username}: {message}")
                        broadcast(f"MESSAGE:{username}: {message}")
            
            except ConnectionResetError:
                break

        print(f"Conexión cerrada con {username}")
        broadcast(f"SERVER_MESSAGE:{username} -- Usuario desconectado")

    def send_file(self, client_socket, file_name):
        file_path = os.path.join("uploads", file_name)
        if file_path:
            file_size = os.path.getsize(file_path)
            try:
                with open(file_path, "rb") as file:
                    file_name = os.path.basename(file_path)
                    header = f"REQUESTED_FILE:{file_name}:{file_size}".encode('utf-8')
                    client_socket.send(header)

                    chunk_size = 8192
                    sent_size = 0
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        client_socket.send(chunk)
                        sent_size += len(chunk)

                    print(f"Archivo {file_name} enviado\n")
            except Exception as e:
                print(f"Error al enviar archivo: {e}\n")

app = ChatApp()

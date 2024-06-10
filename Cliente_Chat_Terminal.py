import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode

class ChatClient:
    def __init__(self):
        self.username = "Usuario"
        self.server_ip = "127.0.0.1"
        self.server_port = 5555

        self.key = b'1234567890123456'

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.iv = b'0000000000000000'

        self.connect_to_server()

    def connect_to_server(self):
        self.username = input("Ingrese su nombre de usuario: ")
        self.server_ip = input("Ingrese la IP del servidor: ")
        self.server_port = int(input("Ingrese el puerto del servidor: "))
        self.key = input("Ingrese la clave: ").encode("utf-8")

        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.send(self.username.encode("utf-8"))
            print(f"Conectado al servidor en {self.server_ip}:{self.server_port} como {self.username}")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"No se pudo conectar al servidor: {e}")
            exit()

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message.startswith(b'MESSAGE:'):
                    message = encrypted_message[len('MESSAGE:'):]
                    parts = message.split(b':', 2)
                    if len(parts) == 3:
                        username = parts[0].decode("utf-8").strip()
                        encrypted_text = parts[2].strip()
                        decrypted_message = self.decrypt_message(encrypted_text)
                        if username != self.username:  # Mostrar solo si el mensaje no es del propio usuario
                            print(f"{username}: {decrypted_message}\n")
                    else:
                        print("Mensaje recibido no válido:", encrypted_message)
                elif encrypted_message.startswith(b'SERVER_MESSAGE:'):
                    message = encrypted_message[len('SERVER_MESSAGE:'):]
                    parts = message.split(b':', 1)
                    if len(parts) == 1:
                        server_message = parts[0].strip()
                        print(f"Servidor: {server_message}\n")
                        print(f" Mensaje del servidor: {message}")
                    else:
                        print("Mensaje del SERVIDOR recibido no válido:", message)
            except Exception as e:
                print("Error al recibir mensaje:", e)
                break

    def send_message(self):
        while True:
            message = input()
            if message:
                encrypted_message = self.encrypt_message(message)
                header = f"MESSAGE:{encrypted_message.decode('utf-8')}".encode('utf-8')
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
    client = ChatClient()
    client.send_message()

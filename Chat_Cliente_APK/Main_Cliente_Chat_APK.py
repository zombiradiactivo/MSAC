import socket
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
# Importar los módulos necesarios de Kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Definir la clase de la aplicación
class ChatClientApp(App):
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Cliente")

        self.username = "Usuario"
        self.server_ip = "127.0.0.1"
        self.server_port = 5555

        # Clave predeterminada
        self.key = b'1234567890123456'

        self.create_widgets()

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Clave para encriptación
        self.iv = b'0000000000000000'  # Vector de inicialización (IV)

    def build(self):
        # Configurar la ventana
        Window.size = (400, 500)
        Window.minimum_width, Window.minimum_height = Window.size

        # Crear el diseño principal de la aplicación
        layout = GridLayout(cols=1, spacing=10, padding=10)

        # Agregar widgets al diseño
        layout.add_widget(Label(text="Nombre de Usuario:"))
        self.username_input = TextInput(text="Usuario")
        layout.add_widget(self.username_input)

        layout.add_widget(Label(text="Clave:"))
        self.key_input = TextInput(password=True)
        layout.add_widget(self.key_input)

        layout.add_widget(Label(text="IP del Servidor:"))
        self.server_input = TextInput(text="127.0.0.1")
        layout.add_widget(self.server_input)

        layout.add_widget(Label(text="Puerto del Servidor:"))
        self.port_input = TextInput(text="5555")
        layout.add_widget(self.port_input)

        self.connect_button = Button(text="Conectar")
        self.connect_button.bind(on_press=self.connect_to_server)
        layout.add_widget(self.connect_button)

        self.messages_text = ScrollView()
        self.messages_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        self.messages_text.add_widget(self.messages_layout)
        layout.add_widget(self.messages_text)

        self.message_input = TextInput()
        self.message_input.bind(on_text_validate=self.send_message)
        layout.add_widget(self.message_input)

        self.send_button = Button(text="Enviar")
        self.send_button.bind(on_press=self.send_message)
        layout.add_widget(self.send_button)

        return layout

    def connect_to_server(self, instance):
        username = self.username_input.text
        key = self.key_input.text
        server_ip = self.server_input.text
        server_port = int(self.port_input.text)

        # Aquí implementarías la lógica para conectar al servidor
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            self.client_socket.send(self.username.encode("utf-8"))
            threading.Thread(target=self.receive_messages).start()
        except Exception as e:
            print("Error", f"No se pudo conectar al servidor: {e}")

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if encrypted_message:
                    decrypted_message = self.decrypt_message(encrypted_message)
                    # Como estamos en un hilo secundario, necesitamos usar Clock.schedule_once
                    # para actualizar la interfaz de usuario desde el hilo principal de Kivy
                    Clock.schedule_once(lambda dt: self.update_messages(decrypted_message))
                    print(f"ENCRIPTADO{encrypted_message}")
                    print(f"DESENCRIPTADO{decrypted_message}")
            except:
                break

    def update_messages(self, decrypted_message):
        # Agregar el mensaje decifrado a la lista de mensajes
        self.messages_layout.add_widget(Label(text=decrypted_message))
        # Mover el ScrollView al final para mostrar el último mensaje
        self.messages_text.scroll_y = 0

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            encrypted_message = self.encrypt_message(message)
            self.client_socket.send(encrypted_message)
            # Limpiar el TextInput después de enviar el mensaje
            self.message_input.text = ''

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
        
# Ejecutar la aplicación
if __name__ == "__main__":
    ChatClientApp().run()

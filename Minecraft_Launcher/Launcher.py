from pycraft import Launcher

# Crea una instancia del Launcher
launcher = Launcher()

# Inicia sesión con tu cuenta de Minecraft (proporciona tu nombre de usuario y contraseña)
launcher.login('tu_correo_electronico', 'tu_contraseña')

# Selecciona la versión que deseas jugar
launcher.launch('1.17.1')  # Puedes cambiar la versión aquí

# Cierra el launcher cuando termines
launcher.close()
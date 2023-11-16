import socket
import threading
# Configuración del cliente
host = '127.0.0.1'  # Debes usar la misma dirección IP del servidor
port = 55555
username = ""
# Crear un objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect((host, port))
print(f"Conectado al servidor en {host}:{port}")

# Función para enviar mensajes al servidor
def send_message(message):
    client_socket.send(message.encode('utf-8'))

# Función para recibir mensajes del servidor
def receive_message():
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        print(f"{data}")

# Iniciar un hilo para recibir mensajes del servidor
receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

# Enviar mensajes al servidor
if username == "":
    username = input("Por favor, cual es tu nombre de usuario?: ")
    send_message(username)
while True:
    #print("Tú:") 
    user_input = input()
    send_message(user_input)

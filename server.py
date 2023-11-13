###############################################
import socket
import threading
import ast
import json
with open('artefactos.json') as arte_file :
  artefactos = arte_file.read()
artefactos = json.loads(artefactos)
# Lista para almacenar los sockets de los clientes
client_sockets = []
usernames = {}
user_items = {}

# Función para manejar la conexión de cada cliente
def handle_client(client_socket, addr):
    print(f"Conexión aceptada desde {addr}")
    # Agregar el socket del cliente a la lista
    client_sockets.append(client_socket)
    #envia msg de bienvenida al usuario
    bienvenida = "¡Bienvenid@ al chat de Granjerxs!"
    client_socket.send(bienvenida.encode('utf-8'))
    #el primer mensaje es el username del usuario
    data = client_socket.recv(1024).decode('utf-8')
    #se crea el mensaje y se hace un broadcast a todos los users sobre la coneccion del usuario
    connected_msg ="[SERVER] " + data +" Se ha conectado."
    sv_broadcast(connected_msg)
    #se guarda el username en el diccionario segun el socket
    usernames[client_socket] = data
    set_client_items(client_socket)
    while True:
        # Espera a recibir datos del cliente
        try:
            data = client_socket.recv(1024).decode('utf-8')
        except:
            #DESCONEXION
            dis_msg = usernames[client_socket] +" Se ha desconectado."
            print("[SERVER] Cliente" + dis_msg)
            client_sockets.remove(client_socket)
            client_socket.close()#ojo
            sv_broadcast(dis_msg)
            break#cierra el thread para el cliente
        if not data:
            break
        # Imprime los datos recibidos y envía la respuesta a todos los clientes
        print(f"Mensaje de {usernames[client_socket]} {addr}: {data}")

        # Enviar el mensaje a todos los clientes
        broadcast(data,client_socket)

    # Cierra la conexión con el cliente y elimina su socket de la lista
    #print(f"Conexión cerrada con {addr}")
    #client_sockets.remove(client_socket)
    #client_socket.close()

# Función para enviar un mensaje a todos los clientes menos al remitente
def broadcast(message,sender):
    message = usernames[sender] + ": " + message
    for client_socket in client_sockets:
        try:
            if client_socket != sender:
                client_socket.send(message.encode('utf-8'))
        except:
            # Si hay un error al enviar el mensaje, cierra la conexión con ese cliente
            client_sockets.remove(client_socket)
            client_socket.close()

# Función para enviar un mensaje a todos los clientes por parte del server
def sv_broadcast(message):
    message = "[SERVER]: " + message
    for client_socket in client_sockets:
        try:
                client_socket.send(message.encode('utf-8'))
        except:
            # Si hay un error al enviar el mensaje, cierra la conexión con ese cliente
            client_sockets.remove(client_socket)
            client_socket.close()
def items_toStr(items):
    str_items = map(str,items)
    ret = ""
    for item in str_items:
        ret = ret + " " + artefactos[item] + " "#no agarra los items
    return ret
    
def set_client_items(client_socket):
    asigned = False
    checked = True
    error = False
    while not asigned:
        #check si los items estan bien declarados
        set_item_msg = "Cuentame, que artefactos tienes?"
        client_socket.send(set_item_msg.encode('utf-8'))
        try:
            items = client_socket.recv(1024).decode('utf-8')
            items = "["+items+"]"
            items = ast.literal_eval(items)
            error = False
        except:
            error = True
            set_item_error_msg = "Ha asignado mal sus items, intentelo otra vez"
            client_socket.send(set_item_error_msg.encode('utf-8'))
        #check si existen los items
        if error == False:
            for item in items:
                if not (item<43 and item>0):
                    set_item_error_msg = "El artefacto " + item + "no existe."
                    client_socket.send(set_item_error_msg.encode('utf-8'))
                    checked = False
            if checked == True: 
                item_str = items_toStr(items)
                set_item_reask = "Estos son sus items?(acepta con 'si'):\n" + item_str
                client_socket.send(set_item_reask.encode('utf-8'))
                res = client_socket.recv(1024).decode('utf-8')
                if res == "si" or res == "SI":
                    user_items[client_socket] = items
                    asigned = True
                    setted_msg = "Sus items fueron asignados"
                    client_socket.send(setted_msg.encode('utf-8'))
def items_toStr(items):
    str_items = map(str,items)
    ret = ""
    for item in str_items:
        ret = ret + artefactos[item] + "\n"
    return ret

    

# Configuración del servidor
host = '127.0.0.1'
port = 55555

# Crear un objeto de socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y puerto
server_socket.bind((host, port))

# Escuchar hasta 5 conexiones simultáneas
server_socket.listen(5)
print(f"Servidor escuchando en {host}:{port}")

while True:
    # Esperar la conexión de un cliente
    client_socket, addr = server_socket.accept()

    # Iniciar un hilo para manejar la conexión del cliente
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()

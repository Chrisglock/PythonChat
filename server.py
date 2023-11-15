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
user_to_socket = {}
user_items = {}
in_trade = {}
error_command_msg = "Ha ocurrido un error con el comando"
emojis = {"smile": ":)","angry":">:C","combito": "O--(’- ’Q)","larva":"(:o)OOOooo" }
mutex_trade = threading.Lock()
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
    connected_msg =data +" Se ha conectado."
    sv_broadcast(connected_msg)
    #se guarda el username en el diccionario segun el socket
    #falta validacion de usuarios repetidos
    usernames[client_socket] = data
    user_to_socket[data] = client_socket
    in_trade[client_socket] = False
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
        if data[0]==":":
            data1 = data.replace(":","")
            handle_commands(data1,client_socket)
        else:
            broadcast(data,client_socket)

    # Cierra la conexión con el cliente y elimina su socket de la lista
    #print(f"Conexión cerrada con {addr}")
    client_sockets.remove(client_socket)
    client_socket.close()

# Función para enviar un mensaje a todos los clientes menos al remitente
def broadcast(message,sender_socket):#sender = sender socket
    message = usernames[sender_socket] + ": " + message
    for client_socket in client_sockets:
        try:
            if client_socket != sender_socket:
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
            #validaciones
            if len(items)<=6:
                for item in items:
                    if not (item<43 and item>0):
                        set_item_error_msg = "El artefacto " + item + "no existe."
                        client_socket.send(set_item_error_msg.encode('utf-8'))
                        checked = False
                ######
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
def items_toStr(items):#items list de int
    str_items = map(str,items)
    ret = "\n"
    for item in str_items:
        ret = ret + artefactos[item] +" ID: " + item +  "\n"
    return ret
def priv_msg(usr_name_sender:str,usr_name_reciever:str,msg:str):
    reciever_socket = user_to_socket[usr_name_reciever]
    msg = "(PRIVADO) " + usr_name_sender + ": " + msg
    reciever_socket.send(msg.encode('utf-8'))

def handle_commands(command: str,requester_socket):
    command = command.split()
    if command[0] == "q":
        exit()
    elif command[0] == "p":
        try:
            sender = usernames[requester_socket]
            priv_msg(sender,command[1],command[2])
        except:
            requester_socket.send(error_command_msg.encode('utf-8'))
    elif command[0] == "u":
        usernames_list = list(usernames.values())
        msg = ""
        for user in usernames_list:
            msg = msg + "°CONECTADO -> " +  user + "\n"
        requester_socket.send(msg.encode('utf-8'))
    elif command[0] == "smile":
        em = emojis["smile"]
        broadcast(em,requester_socket)
    elif command[0] == "angry":
        em = emojis["angry"]
        broadcast(em,requester_socket)
    elif command[0] == "combito":
        em = emojis["combito"]
        broadcast(em,requester_socket)
    elif command[0] == "larva":
        em = emojis["larva"]
        broadcast(em,requester_socket)
    elif command[0] == "myitems":
        msg = items_toStr(user_items[requester_socket])
        requester_socket.send(msg.encode('utf-8'))
    elif command[0] == "offer":
        try:
            objetive = user_to_socket[command[1]]
            trade_item(requester_socket,objetive,command[2],command[3])
        except:
            requester_socket.send("error en trade".encode('utf-8'))
    else:
        requester_socket.send("comando desconocido\n".encode('utf-8'))
    return 0
def trade_item(requester,objetive,ritem,oitem):
    #aplicar todas las validaciones
    #el objetivo ya está en un trade, intente más tarde
    #ambos users tienen los items
    #ambos sockets se ponen en estado trading
    #antes de aplicar el trade se pide validacion al objetivo
    
    if in_trade[requester] == True:
        requester.send("Tienes un tradeo pendiente".encode('utf-8'))
        if in_trade[objetive] == True:
            requester.send("El usuario objetivo ya está tradeando, intente mas tarde\n".encode('utf-8'))
        else:
            in_trade[requester] = True
            in_trade[objetive] = True     
            ritem = int(ritem)
            oitem = int(oitem)
            mutex_trade.acquire()
            if ritem in user_items[requester] :
                if oitem in user_items[objetive]:
                    user_items[requester].remove(ritem)
                    user_items[requester].append(oitem)
                    user_items[objetive].remove(oitem)
                    user_items[objetive].append(ritem)
                    requester.send("Tradeo hecho".encode('utf-8'))
                    in_trade[requester] = False
                    in_trade[objetive] = False
            else:
                requester.send("No ".encode('utf-8'))
            mutex_trade.release()
def trading_manager():
    return 0
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

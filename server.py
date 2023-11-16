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
trade_response = {}
error_command_msg = "[SERVER] Ha ocurrido un error con el comando"
emojis = {"smile": ":)","angry":">:C","combito": "O--(’- ’Q)","larva":"(:o)OOOooo","erai":"(╯°□°)--︻╦╤─ - - - " }
success_trade_msg = "\nIntercambio exitoso!"
reject_trade_msg = "\nIntercambio rechazadoX!"
mutex_trade = threading.Lock()
# Función para manejar la conexión de cada cliente
def handle_client(client_socket, addr):
    print(f"Conexión aceptada desde {addr}")
    # Agregar el socket del cliente a la lista
    client_sockets.append(client_socket)
    #envia msg de bienvenida al usuario
    bienvenida = "[SERVER] ¡Bienvenid@ al chat de Granjerxs!\n" + "Ingrese su nombre de usuario:\n" 
    client_socket.send(bienvenida.encode('utf-8'))
    #el primer mensaje es el username del usuario
    try:
        data = client_socket.recv(1024).decode('utf-8')
    except:
        print(f"Desconexion previa username {client_socket}")
        return
    #se crea el mensaje y se hace un broadcast a todos los users sobre la coneccion del usuario
    connected_msg =data +" Se ha conectado."
    sv_broadcast(connected_msg)
    #se guarda el username en el diccionario segun el socket
    #falta validacion de usuarios repetidos
    usernames[client_socket] = data
    user_to_socket[data] = client_socket
    in_trade[client_socket] = False
    trade_response[client_socket] = "no_response"
    try:
        data = set_client_items(client_socket)
    except:
        print(f"Desconexion durante set items {client_socket}")
        return
    while True:
        # Espera a recibir datos del cliente
        try:
            data = client_socket.recv(1024).decode('utf-8')
        except:
            #DESCONEXION
            dis_msg = usernames[client_socket] +" Se ha desconectado."
            print("[SERVER] Cliente " + dis_msg)
            client_sockets.remove(client_socket)
            client_socket.close()#ojo
            sv_broadcast(dis_msg)
            return#cierra el thread para el cliente
        if not data:
            return
        # Imprime los datos recibidos y envía la respuesta a todos los clientes
        print(f"Mensaje de {usernames[client_socket]} {addr}: {data}")

        # maneja el mensaje
        if data[0]==":":
            data1 = data.replace(":","")
            handle_commands(data1,client_socket)
        else:
            broadcast(data,client_socket)
# Función para enviar un mensaje a todos los clientes menos al remitente
def broadcast(message,sender_socket):#sender = sender socket
    message = usernames[sender_socket] + ": " + message
    for client_socket in client_sockets:
        try:
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
    while not asigned:
        #check si los items estan bien declarados
        error = False
        checked = True
        set_item_msg = "[SERVER] Cuentame, que artefactos tienes?"
        client_socket.send(set_item_msg.encode('utf-8'))
        try:
            items = client_socket.recv(1024).decode('utf-8')
            items = "["+items+"]"
            items = ast.literal_eval(items)
            error = False
        except:
            error = True
            set_item_error_msg = "[SERVER] Ha asignado mal sus items, intentelo otra vez"
            client_socket.send(set_item_error_msg.encode('utf-8'))
        #check si existen los items
        if error == False:
            #validaciones
            if len(items)<=6:
                for item in items:
                    if not (item<43 and item>0):
                        set_item_error_msg = f"[SERVER] El artefacto {item} no existe."
                        client_socket.send(set_item_error_msg.encode('utf-8'))
                        checked = False
                ######
                if checked == True: 
                    item_str = items_toStr(items)
                    set_item_reask = "[SERVER] Estos son sus items? si/no:\n" + item_str
                    client_socket.send(set_item_reask.encode('utf-8'))
                    res = client_socket.recv(1024).decode('utf-8')
                    if res == "si" or res == "SI":
                        user_items[client_socket] = items
                        asigned = True
                        setted_msg = "[SERVER] Sus items fueron asignados"
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
    elif command[0] == "erai":
        em = emojis["erai"]
        broadcast(em,requester_socket)
    elif command[0] == "artefactos":
        msg = items_toStr(user_items[requester_socket])
        requester_socket.send(msg.encode('utf-8'))
    elif command[0] == "artefacto":
        try:
            msg = f"[SERVER]: {artefactos[command[1]]}"
            requester_socket.send(msg.encode('utf-8'))
        except:
            requester_socket.send("\n[SERVER] artefacto invalido".encode('utf-8'))
    elif command[0] == "offer":
        try:
            objetive = user_to_socket[command[1]]
            if requester_socket != objetive:
                trader_thread = threading.Thread(target=trade_item, args=(requester_socket,objetive,command[2],command[3]))
                trader_thread.start()
            else:
                requester_socket.send("[SERVER] error en trade".encode('utf-8'))
        except:
            requester_socket.send("[SERVER] error en trade".encode('utf-8'))
    elif command[0] == "accept":
        if in_trade[requester_socket] == True:
            trade_response[requester_socket] = "accept"
        else:
            requester_socket.send("[SERVER] No estas en un trade".encode('utf-8'))
    elif command[0] == "reject":
        if in_trade[requester_socket] == True:
            trade_response[requester_socket] = "reject"
        else:
            requester_socket.send("[SERVER] No estas en un trade".encode('utf-8'))
    else:
        requester_socket.send("[SERVER] comando desconocido\n".encode('utf-8'))
def trade_item(requester,objetive,ritem,oitem):#se ejecuta  como un nuevo thread
    #aplicar todas las validaciones
        #el objetivo ya está en un trade, intente más tarde
        #ambos users tienen los items
        #ambos sockets se ponen en estado trading
        #antes de aplicar el trade se pide validacion al objetivo
    if in_trade[requester] != True:
        if in_trade[objetive] != True:
            mutex_trade.acquire()#se pide el mutex 
            in_trade[requester] = True
            in_trade[objetive] = True     
            mutex_trade.release()
            trade_msg = f"[SERVER] has hecho TRADE OFFER a {usernames[requester]}\n TU item: ID:{oitem} {artefactos[oitem]}\n POR item ID:{ritem} {artefactos[ritem]} DE {usernames[requester]}"
            trade_msg_req = f"[SERVER] HAS OFRECIDO\n TU item: ID:{ritem} {artefactos[ritem]}\n POR item ID:{oitem} {artefactos[oitem]} DE {usernames[objetive]}"
            requester.send(trade_msg_req.encode('utf-8'))
            objetive.send(trade_msg.encode('utf-8'))
            ############ busy waiting, se bloquea hasta que le llegue una respuesta
            while trade_response[objetive] != "accept" and trade_response[objetive] != "reject":
                pass#NADA XD
            ############
            if trade_response[objetive] == "accept":
                mutex_trade.acquire()#se pide el mutex 
                ritem = int(ritem)
                oitem = int(oitem)
                if ritem in user_items[requester]:
                    if oitem in user_items[objetive]:
                        #request aceptar o declinar trade
                        user_items[requester].remove(ritem)
                        user_items[requester].append(oitem)
                        user_items[objetive].remove(oitem)
                        user_items[objetive].append(ritem)
                        requester.send("[SERVER] Tradeo hecho".encode('utf-8'))
                    else:
                        requester.send("\n[SERVER] objetivo no tiene el item".encode('utf-8'))
                else:
                    requester.send("\n[SERVER] No tienes este item".encode('utf-8'))
                trade_response[objetive] == "no_response"
                requester.send(success_trade_msg.encode('utf-8'))
                objetive.send(success_trade_msg.encode('utf-8'))
                in_trade[requester] = False
                in_trade[objetive] = False
            elif trade_response[objetive] == "reject":
                trade_response[objetive] == "no_response"
                in_trade[requester] = False
                in_trade[objetive] = False
                requester.send(reject_trade_msg.encode('utf-8'))
                objetive.send(reject_trade_msg.encode('utf-8'))
            mutex_trade.release()
        else:
            requester.send("[SERVER] El usuario objetivo ya está tradeando, intente mas tarde\n".encode('utf-8'))
    else:
        requester.send("[SERVER] Tienes un tradeo pendiente".encode('utf-8'))
    return
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

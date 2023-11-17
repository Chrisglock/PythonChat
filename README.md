# PythonChat
Este es un chat hecho con Python,Socket,Threading y PyQt6

#   Tema: Chat de Granjer@s

Este proyecto implementa un sistema de chat en Python que permite la comunicación entre varios usuarios. Además del chat básico, el sistema admite funcionalidades adicionales como mensajes privados y la posibilidad de realizar intercambios comerciales entre usuarios.

## Contenido del Repositorio

- **server.py**: Este script actúa como servidor central, gestionando las conexiones y facilitando la comunicación entre los clientes.
- **client.pyw**: El script del cliente, que presenta una interfaz gráfica desarrollada con PyQt6 para hacer la interacción más amigable.
- **chat.ui**: Archivo que contiene el codigo de la interfaz del chat.
- **artefactos.json**: Archivo que contiene todos los items tradeables.


## Dependencias

Asegúrate de tener instaladas las siguientes dependencias antes de ejecutar el proyecto:
socket: Módulo para la creación y manipulación de sockets.
threading: Módulo para la creación de hilos para la recepción continua de mensajes.
sys: Módulo para acceder a variables y funciones específicas del sistema.
PyQt6: Biblioteca para el desarrollo de interfaces gráficas en Qt.

Configuración
El cliente se conecta al servidor en 127.0.0.1 y el puerto 55555.

Uso
Ejecuta el servidor mediante el comando python server.py.
Conecta clientes utilizando el script python client.pyw.
Ingresa un nombre de usuario a través de la interfaz gráfica del cliente.
Comienza a chatear y explora las funcionalidades adicionales.
Comandos Soportados por el Servidor
El servidor admite varios comandos que permiten a los usuarios realizar acciones específicas. Aquí hay algunos ejemplos:
todos los comandos deben llevar el prefijo ":", es decir , :u mostraría todos los usuarios conectados.
q Salir del servidor.
p [usuario] [mensaje]: Enviar un mensaje privado a otro usuario.
u Mostrar la lista de usuarios conectados.
smile, angry, combito, larva, erai, ?: Enviar emoticones a todos los usuarios.
artefactos: Mostrar la lista de artefactos del usuario.
artefacto [ID]: Obtener información sobre un artefacto específico.
offer [usuario] [ID_enviar] [ID_recibir]: Ofrecer un intercambio a otro usuario.
accept Aceptar una oferta de intercambio pendiente.
reject Rechazar una oferta de intercambio pendiente.

Funciones Importantes en el Servidor
handle_client: Función para manejar la conexión de cada cliente.
broadcast: Envía un mensaje a todos los clientes excepto al remitente.
sv_broadcast: Envía un mensaje a todos los clientes en nombre del servidor.
set_client_items: Asigna artefactos al cliente al conectarse.
handle_commands: Maneja los comandos ingresados por los usuarios.
trade_item: Realiza un intercambio de artefactos entre dos usuarios.
Cliente con Interfaz Gráfica (client.pyw)
Descripción
Este script implementa un cliente de chat en Python utilizando la biblioteca PyQt6 para la interfaz gráfica y sockets para la comunicación con el servidor. Permite que el usuario se conecte al servidor, ingrese un nombre de usuario y participe en un chat gráfico.

Licencia
Este proyecto está bajo la Licencia MIT.

Desarrollador: Chrisglock

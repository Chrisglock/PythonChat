import socket
import threading
import sys
from PyQt6 import QtGui, QtWidgets, uic
from PyQt6.QtCore import pyqtSlot, QThread, QObject, pyqtSignal

# Configuración del cliente
host = '127.0.0.1'  # Debes usar la misma dirección IP del servidor
port = 55555

# Crear un objeto de socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect((host, port))
print(f"Conectado al servidor en {host}:{port}")


class ReceiveMessage(QObject):
    message_received = pyqtSignal(str)

    @pyqtSlot()
    def receive_message(self):
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            self.message_received.emit(data)


class Ventana(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('chat.ui')
        self.ui.setWindowIcon(QtGui.QIcon('hat.png'))
        self.ui.show()
        self.current_chat = ""
        self.username = ""

        self.receive_thread = QThread()
        self.receiver = ReceiveMessage()
        self.receiver.moveToThread(self.receive_thread)
        self.receive_thread.started.connect(self.receiver.receive_message)
        self.receiver.message_received.connect(self.set_text_chat)

        # Iniciar un hilo para recibir mensajes del servidor
        self.receive_thread.start()

        # Se conecta la señal del botón para enviar mensajes al servidor
        self.ui.user_text.returnPressed.connect(self.get_text)
        self.ui.send.clicked.connect(self.get_text)

    @pyqtSlot()
    def get_text(self):
        if self.username == "":
            self.username = self.ui.user_text.text()
            send_message(f"{self.username}")
            self.ui.user_text.clear()
            self.ui.setWindowTitle(f"Chat granjeros [{self.username}]")
        else:
            user_input = self.ui.user_text.text()
            self.ui.user_text.clear()
            send_message(user_input)

    @pyqtSlot(str)
    def set_text_chat(self, msg):
        self.current_chat += "\n" + msg
        self.ui.chat_text.setText(self.current_chat)


# Función para enviar mensajes al servidor
def send_message(message):
    client_socket.send(message.encode('utf-8'))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana()
    sys.exit(app.exec())

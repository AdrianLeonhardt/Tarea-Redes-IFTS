import socket
import threading

HOST="127.0.0.1"
PORT= 12345

# Inicializar socket del cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

# Función para recibir mensajes del servidor
def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            print(mensaje)
        except:
            print("Error al recibir el mensaje.")
            cliente.close()
            break

# Función para enviar mensajes al servidor
def enviar_mensajes():
    while True:
        try:
            mensaje = input()
            cliente.send(mensaje.encode('utf-8'))
            if mensaje == "/exit":
                break
        except:
            break

# Iniciar hilos para recibir 
receive_thread = threading.Thread(target=recibir_mensajes)
receive_thread.start()

# Iniciar hilos para enviar mensajes
write_thread = threading.Thread(target=enviar_mensajes)
write_thread.start()
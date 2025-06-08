import socket # Para crear la conexión de red (cliente-servidor)
import threading # Para ejecutar múltiples tareas al mismo tiempo (hilos)

# Dirección IP y puerto del servidor al que el cliente se conectará
HOST="127.0.0.1"
PORT= 12345

# Inicializa el socket del cliente como un socket TCP/IP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta el cliente al servidor especificado por HOST y PORT
cliente.connect((HOST, PORT))

# Función para recibir mensajes del servidor
def recibir_mensajes():
    while True:
        try:
            # Recibe hasta 1024 bytes desde el servidor y decofica bytes a string
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
            # Espera al input del usuario
            mensaje = input()
            cliente.send(mensaje.encode('utf-8'))
            # Si el usuario escribe "/exit", termina la comunicación
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

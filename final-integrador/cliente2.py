import socket         # Para crear la conexión de red cliente-servidor
import threading      # Para manejar recibir y enviar mensajes al mismo tiempo

# IP y puerto del servidor
HOST = "127.0.0.1"
PORT = 12345

# Crear socket del cliente (TCP/IP)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
cliente.connect((HOST, PORT))

# Función para recibir mensajes del servidor
def recibir():
    while True:
        try:
            # Recibe datos del servidor
            mensaje = cliente.recv(4096).decode('utf-8')
            if not mensaje:
                print("Conexión cerrada por el servidor.")
                break
            print(mensaje, end='')  # Mostrar mensaje recibido
        except:
            print("Error al recibir el mensaje.")
            cliente.close()
            break

# Función para enviar mensajes al servidor
def enviar():
    while True:
        try:
            # Leer entrada del usuario
            mensaje = input()
            cliente.send(mensaje.encode('utf-8'))

            # Si el usuario quiere salir, cerramos
            if mensaje.lower() == '/adios':
                print("Cerrando conexión...")
                break
        except:
            break

# Crear e iniciar hilo para recibir mensajes
hilo_lectura = threading.Thread(target=recibir)
hilo_lectura.start()

# Crear e iniciar hilo para enviar mensajes
hilo_envio = threading.Thread(target=enviar)
hilo_envio.start()

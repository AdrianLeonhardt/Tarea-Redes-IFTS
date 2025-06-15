import socket  # Para crear la conexión de red (cliente-servidor)
import threading # Para ejecutar múltiples tareas al mismo tiempo (hilos)

# Dirección IP y puerto del servidor al que el cliente se conectará
HOST = "127.0.0.1"
PORT = 12345

# Acumulador de usuarios conectados
clientes = {}

# Inicializa el socket del servidor como TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Asocia el socket a la IP y puerto definidos
servidor.bind((HOST, PORT))
# Comienza a escuchar conexiones entrantes
servidor.listen()

menu = """
Menú de opciones, Escribe el comando seguido de Enter:
/login + tu <nombre>        → Iniciar sesión
/send + <usuario> + <msg>   → Enviar mensaje privado
/sendall <msg>              → Enviar mensaje a todos
/show                       → Mostrar usuarios conectados
/exit                       → Salir
"""

# Función para enviar a todos un mensaje
def broadcast(message):
    for cliente in clientes.values():
        cliente.send(message.encode())

# Función para manejar la conexión de un cliente
def manejar_cliente(cliente):
    usuario = None # Inicializa el nombre del usuario como None
    cliente.send(menu.encode()) # Envía el menú de ayuda al cliente

    while True:
        try:
            # Espera recibir un mensaje del cliente
            mensaje = cliente.recv(1024).decode().strip()
             # Si el mensaje está vacío, se rompe el bucle
            if not mensaje:
                break
            # Comando para iniciar sesión con un nombre de usuari
            if mensaje.startswith("/login"):
                usuario = mensaje.split(" ", 1)[1]  # Extrae el nombre
                clientes[usuario] = cliente # Registra el usuario y su socket
                cliente.send(f"Sesión iniciada como {usuario}\n".encode())
            # Comando para enviar mensaje privado a otro usuario
            elif mensaje.startswith("/send "):
                destino, msg = mensaje.split(" ", 2)[1:] # Extrae destinatario y mensaje
                clientes[destino].send(f"[Privado de {usuario}]: {msg}\n".encode())
            # Comando para enviar mensaje a todos 
            elif mensaje.startswith("/sendall "):
                msg = mensaje.split(" ", 1)[1] # Extrae el mensaje
                for u, c in clientes.items():
                    if u != usuario: # Evita enviar el mensaje a sí mismo
                        c.send(f"[{usuario} → todos]: {msg}\n".encode())
            # Comando para mostrar todos los usuarios conectados
            elif mensaje == "/show":
                lista = "\n".join(clientes.keys()) # Lista de nombres de usuarios conectados
                cliente.send(f"Usuarios conectados:\n{lista}\n".encode())
            # Comando para salir del chat
            elif mensaje == "/exit":
                cliente.send("Saliendo...\n".encode())
                break

            else:
                cliente.send("Comando no reconocido.\n".encode())

        except:
            break # Si hay error en cualquier paso, rompe el bucle

    # Cierre de sesión
    if usuario and usuario in clientes:
        del clientes[usuario]
        broadcast(f"{usuario} ha salido del chat.\n")
    cliente.close()

# Función para aceptar conexiones de clientes
def aceptar_conexiones():
    print(f"[✓] Servidor escuchando en {HOST}:{PORT}")
    while True:
        cliente, direccion = servidor.accept() # Espera una nueva conexión
        print(f"[+] Nueva conexión desde {direccion}")
        # Crea un hilo para manejar al nuevo cliente y lo inicia
        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.start()
# Inicia el servidor llamando a la función que acepta conexiones
aceptar_conexiones()


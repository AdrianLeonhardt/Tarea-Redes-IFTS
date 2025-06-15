import socket 
import threading

HOST = "127.0.0.1"
PORT = 12345

# Acumulador de usuarios conectados
clientes = {}

# Inicializar socket del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

menu = """
Menú de opciones, Escribe el comando seguido de Enter:
/login + tu <nombre>        → Iniciar sesión
/send + <usuario> + <msg>   → Enviar mensaje privado
/sendall <msg>              → Enviar mensaje a todos
/show                       → Mostrar usuarios conectados
/exit                       → Salir
"""

# Función para enviar a todos
def broadcast(message):
    for cliente in clientes.values():
        cliente.send(message.encode())

# Función para manejar la conexión de un cliente
def manejar_cliente(cliente):
    usuario = None
    cliente.send(menu.encode())

    while True:
        try:
            mensaje = cliente.recv(1024).decode().strip()

            if not mensaje:
                break

            if mensaje.startswith("/login"):
                usuario = mensaje.split(" ", 1)[1]
                clientes[usuario] = cliente
                cliente.send(f"Sesión iniciada como {usuario}\n".encode())

            elif mensaje.startswith("/send "):
                destino, msg = mensaje.split(" ", 2)[1:]
                clientes[destino].send(f"[Privado de {usuario}]: {msg}\n".encode())

            elif mensaje.startswith("/sendall "):
                msg = mensaje.split(" ", 1)[1]
                for u, c in clientes.items():
                    if u != usuario:
                        c.send(f"[{usuario} → todos]: {msg}\n".encode())

            elif mensaje == "/show":
                lista = "\n".join(clientes.keys())
                cliente.send(f"Usuarios conectados:\n{lista}\n".encode())

            elif mensaje == "/exit":
                cliente.send("Saliendo...\n".encode())
                break

            else:
                cliente.send("Comando no reconocido.\n".encode())

        except:
            break

    # Cierre de sesión
    if usuario and usuario in clientes:
        del clientes[usuario]
        broadcast(f"{usuario} ha salido del chat.\n")
    cliente.close()

# Función para aceptar conexiones de clientes
def aceptar_conexiones():
    print(f"[✓] Servidor escuchando en {HOST}:{PORT}")
    while True:
        cliente, direccion = servidor.accept()
        print(f"[+] Nueva conexión desde {direccion}")
        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.start()

aceptar_conexiones()


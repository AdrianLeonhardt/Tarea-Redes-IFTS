import socket             # Para la conexión de red cliente-servidor
import threading          # Para manejar múltiples clientes simultáneamente (hilos)
import requests           # Para hacer peticiones a la API de GitHub
import mysql.connector    # Para conectarse a la base de datos MySQL

# Configuración del servidor (IP y puerto)
HOST = "127.0.0.1"
PORT = 12345

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="final_redes"
)

# Cursor para ejecutar consultas SQL
sql = db.cursor()

# Crear el socket TCP/IP del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))     # Asignar IP y puerto al socket
servidor.listen()               # Poner el servidor en modo escucha

# Función que obtiene datos del usuario GitHub y los guarda en la base de datos
def obtener_datos(usuario):
    # Verificar que el usuario exista en GitHub
    url_usuario = f"https://api.github.com/users/{usuario}"
    try:
        resp_usuario = requests.get(url_usuario)
        if resp_usuario.status_code != 200:
            return False, f"Usuario '{usuario}' no encontrado en GitHub.\n"
    except Exception as e:
        return False, f"Error al conectar con GitHub: {e}\n"

    # Obtener los repositorios del usuario
    try:
        url_repos = f"https://api.github.com/users/{usuario}/repos"
        resp_repos = requests.get(url_repos, params={"sort": "created", "direction": "desc"})
        repos = resp_repos.json()
    except Exception as e:
        return False, f"Error al obtener repositorios: {e}\n"

    # Guardar los primeros 5 repositorios en la base de datos
    guardados_repos = 0
    for repo in repos[:5]:
        sql.execute("""
            INSERT IGNORE INTO repositorios (id, name, html_url, description, created_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            repo['id'],
            repo['name'],
            repo['html_url'],
            repo['description'],
            repo['created_at']
        ))
        guardados_repos += 1

    # Obtener la lista de seguidores del usuario
    try:
        url_followers = f"https://api.github.com/users/{usuario}/followers"
        resp_followers = requests.get(url_followers)
        followers = resp_followers.json()
    except Exception as e:
        return False, f"Error al obtener followers: {e}\n"

    # Guardar los seguidores en la base de datos
    guardados_followers = 0
    for follower in followers:
        sql.execute("""
            INSERT IGNORE INTO followers (id, login, html_url)
            VALUES (%s, %s, %s)
        """, (
            follower['id'],
            follower['login'],
            follower['html_url']
        ))
        guardados_followers += 1

    # Confirmar todos los INSERT en la base de datos
    db.commit()

    # Mensaje de resumen
    msg = (
        f"Datos de {usuario} guardados correctamente.\n"
        f"Repositorios guardados: {guardados_repos}\n"
        f"Followers guardados: {guardados_followers}\n"
    )
    return True, msg

# Función que envía un mensaje completo al cliente
def enviar(cliente, mensaje):
    cliente.sendall(mensaje.encode())

# Función que maneja la interacción con un solo cliente
def manejar_cliente(cliente):
    try:
        # Solicita el nombre del usuario GitHub
        enviar(cliente, "Bienvenido. Ingresa tu nombre de usuario GitHub:\n")
        nombre = cliente.recv(1024).decode().strip()

        # Intenta obtener y guardar los datos del usuario
        exito, respuesta = obtener_datos(nombre)
        enviar(cliente, respuesta)
        if not exito:
            cliente.close()
            return

        # Mostrar menú de comandos disponibles
        menu = (
            "\nMenú de opciones:\n"
            "  /repos   → Ver repositorios guardados\n"
            "  /adios   → Salir del sistema\n"
        )
        enviar(cliente, menu)

        # Bucle para escuchar comandos del cliente
        while True:
            comando = cliente.recv(1024).decode().strip()
            if not comando:
                break

            # Mostrar repositorios guardados en la base de datos
            if comando == "/repos":
                sql.execute("SELECT name, html_url FROM repositorios")
                resultados = sql.fetchall()
                if not resultados:
                    enviar(cliente, "No hay repositorios guardados para este usuario.\n")
                else:
                    lista = "Repositorios:\n"
                    for nombre, url in resultados:
                        lista += f"- {nombre} ({url})\n"
                    enviar(cliente, lista)

            # Comando para cerrar la conexión del cliente
            elif comando == "/adios":
                enviar(cliente, "Adiós.\n")
                break

            # Comando mal ingresado
            else:
                enviar(cliente, "Comando no reconocido. Usa /repos o /adios\n")

    except Exception as e:
        print(f"Error con cliente: {e}")
    finally:
        cliente.close()  # Cierra la conexión con el cliente

# Función principal que acepta múltiples conexiones
def aceptar_conexiones():
    print(f"Servidor activo en {HOST}:{PORT}")
    while True:
        cliente, direccion = servidor.accept()
        print(f"[+] Nueva conexión desde {direccion}")
        hilo = threading.Thread(target=manejar_cliente, args=(cliente,))
        hilo.start()

# Iniciar servidor
aceptar_conexiones()

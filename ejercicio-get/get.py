import requests
import mysql.connector

# Conexion a la base de datos
conexion = mysql.connector.connect(
        host='localhost',
        user='root',             
        password='',            
        database='api_get_python'
    )
# Crea un cursor para ejecutar consultas SQL
guardarEnBd = conexion.cursor()

# Ingreso de usuario de GitHub
usuario = input("Ingrese el nombre de usuario de GitHub: ")

# Introduce el nombre del usuario en el link del Repositorio
url = f"https://api.github.com/users/{usuario}/repos"
# Define parámetros para ordenar los repositorios por fecha de creación, de más reciente a más antiguo
params = {"sort": "created", "direction": "desc"}

# Intenta hacer una petición GET a la API de GitHub para obtener los repositorios del usuario
try:
    response = requests.get(url, params=params)
# Si ocurre un error en la petición termina el programa
except requests.exceptions.RequestException as e:
    print(f"Error al conectarse a la API de GitHub: {e}")
    exit()

# Convierte la respuesta JSON de la API en una lista de repositorios
repositorios = response.json()
# Contador para saber cuántos repositorios se guardaron
repos_guardados = 0 
print(f"Repositorios de {usuario}:")

# Recorre los primeros 5 repositorios de la lista
for repo in repositorios[:5]:
    print(f"- {repo['name']} ({repo['html_url']})")

# Inserta los datos del repositorio en la tabla 'repositorios' de la base de datos
    guardarEnBd.execute("""
        INSERT IGNORE INTO repositorios (id, name, html_url, description, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        repo['id'],             # ID único del repositorio
        repo['name'],           # Nombre del repositorio
        repo['html_url'],       # URL al repositorio en GitHub
        repo['description'],    # Descripción del repositorio
        repo['created_at']      # Fecha de creación
    ))
    repos_guardados += 1        # Aumenta el contador de repositorios guardados

# Muestra cuántos repositorios fueron guardados en la base de datos
print(f"{repos_guardados} repositorios guardados.")

# Introduce el nombre del usuario en el link del Repositorio para ver los seguidores
url_followers = f"https://api.github.com/users/{usuario}/followers"

# Intenta hacer la petición a la API para obtener los seguidores
try:
    response_followers = requests.get(url_followers)
# Captura errores si hubo problemas al obtener los seguidores
except requests.exceptions.RequestException as e:
    print(f"Error al obtener followers: {e}")
    exit()

# Convierte la respuesta JSON en una lista de seguidores
followers = response_followers.json()
# Contador para saber cuántos seguidores se guardaron
followers_guardados = 0

# Recorre cada seguidor recibido en la respuesta
for follower in followers:
# Inserta los datos del seguidor en la tabla 'followers' de la base de datos
    guardarEnBd.execute("""
        INSERT IGNORE INTO followers (id, login, html_url)
        VALUES (%s, %s, %s)
    """, (
        follower['id'],         # ID único del seguidor
        follower['login'],      # Nombre de usuario del seguidor
        follower['html_url']    # URL del perfil del seguidor
    ))
    followers_guardados += 1    # Aumenta el contador de seguidores guardados

# Muestra cuántos seguidores fueron guardados en la base de datos
print(f"{followers_guardados} followers guardados.")

# Guarda todos los cambios realizados en la base de datos
conexion.commit()
# Cierra el cursor y la conexión a la base de datos
guardarEnBd.close()
conexion.close()

print("¡Datos guardados exitosamente!")

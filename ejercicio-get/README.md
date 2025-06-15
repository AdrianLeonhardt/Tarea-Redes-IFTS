===============================================
EJERCICIO: API DE GITHUB + MYSQL
===============================================

1) Realizar un programa que permita el ingreso de un usuario de GitHub y guarde los 
   datos de sus repositorios en una tabla llamada `repositorios` y de sus followers 
   en una tabla llamada `followers`, utilizando MySQL como base de datos.

================================================
INSTRUCCIONES PARA EJECUTAR EL PROYECTO
================================================

-----------------------------------------------
1: CREAR UN ENTORNO VIRTUAL
-----------------------------------------------

Esto mantiene las dependencias aisladas del resto del sistema.

**Windows:**
    python -m venv venv

**Linux / macOS:**
    python3 -m venv venv

-----------------------------------------------
2: ACTIVAR EL ENTORNO VIRTUAL
-----------------------------------------------

**Windows:**
    venv\Scripts\activate

**Linux / macOS:**
    source venv/bin/activate

-----------------------------------------------
3: CREAR EL ARCHIVO requirements.txt
-----------------------------------------------

Crea un archivo llamado `requirements.txt` en la carpeta del proyecto con este contenido:

    requests
    mysql-connector-python

-----------------------------------------------
4: INSTALAR DEPENDENCIAS
-----------------------------------------------

Con el entorno virtual activo, instala las librerías necesarias:

    pip install -r requirements.txt

(Opcional: Si ya instalaste las librerías manualmente, puedes generar el archivo con:)
    pip freeze > requirements.txt

-----------------------------------------------
5: CONFIGURAR LA BASE DE DATOS EN MYSQL
-----------------------------------------------

1. Abrir cliente MySQL
2. Ejecutar las siguientes instrucciones SQL:

    CREATE DATABASE api_get_python;

    USE api_get_python;

    CREATE TABLE repositorios (
        id BIGINT PRIMARY KEY,
        name VARCHAR(255),
        html_url VARCHAR(500),
        description TEXT,
        created_at DATETIME
    );

    CREATE TABLE followers (
        id BIGINT PRIMARY KEY,
        login VARCHAR(255),
        html_url VARCHAR(500)
    );

-----------------------------------------------
PASO 6: EJECUTAR EL SCRIPT
-----------------------------------------------

Con el entorno virtual activo, ejecuta el script de Python:

    python "nombre_del_script.py"

-----------------------------------------------
PASO 7: FINALIZAR
-----------------------------------------------

Cuando termines, puedes desactivar el entorno virtual con:

    deactivate

-----------------------------------------------
RESULTADO ESPERADO:
===============================================

- Se solicitará el nombre de usuario de GitHub.
- Se consultarán los primeros 5 repositorios y todos los seguidores de ese usuario.
- Se guardarán en las tablas `repositorios` y `followers` de tu base de datos MySQL.
- Se mostrará en pantalla cuántos repositorios y seguidores fueron guardados.

===============================================

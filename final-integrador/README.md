# TP Integrador – Redes IFTS

## Consigna

1. Realizar un programa **Cliente-Servidor con sockets concurrente** donde el cliente debe enviar su nombre de usuario de GitHub.  
2. El **servidor** debe obtener los datos del usuario desde la API pública de GitHub y:
   - Guardar sus **repositorios** en una tabla MySQL llamada `repositorios`.
   - Guardar sus **seguidores** en una tabla llamada `followers`.
3. Cuando el cliente envíe el comando `/repos`, el servidor debe responder con la lista de sus repositorios guardados.
4. Si el cliente envía el comando `/adios`, el servidor debe responder con un mensaje de despedida y **cerrar la conexión**.

---

## Tecnologías utilizadas

- **Python 3**
- **Sockets TCP/IP**
- **Multithreading** para manejar múltiples clientes concurrentemente
- **API REST de GitHub** (`requests`)
- **MySQL** como base de datos para persistencia

---

## Servidor (`servidor.py`)

- Acepta múltiples conexiones simultáneamente usando `threading`.
- Solicita al cliente el nombre de usuario de GitHub.
- Usa la API de GitHub para obtener:
  - Repositorios (máximo 5)
  - Seguidores
- Guarda la información en MySQL.


## Ejecución 

1. pip install requests mysql-connector-python
2. Ejecutar servidor: python servidor.py
3. Ejecutar cliente: python cliente.py

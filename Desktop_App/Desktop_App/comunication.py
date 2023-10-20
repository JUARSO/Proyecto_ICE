import socket

# Variable global para almacenar la conexión con el ESP32
esp32_socket = None

# Función para establecer una conexión con el ESP32
def conectar_a_esp32(ip, puerto):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, puerto))
    return s

# Función para enviar datos al ESP32 y recibir una respuesta
def enviar_recibir_datos(sock, datos):
    sock.sendall(datos.encode('utf-8'))
    datos_recibidos = sock.recv(1024)
    return datos_recibidos.decode('utf-8')

# Función para cerrar una conexión
def cerrar_conexion(sock):
    sock.close()

# Función para inicializar la conexión con el ESP32
def inicializar_conexion_esp32():
    global esp32_socket
    esp32_ip = "192.168.1.100"
    esp32_puerto = 1234
    esp32_socket = conectar_a_esp32(esp32_ip, esp32_puerto)

# Función para enviar datos al ESP32
def enviar_datos_al_esp32(datos):
    global esp32_socket
    if esp32_socket is None:
        raise ValueError("La conexión con el ESP32 no está inicializada. Llama a inicializar_conexion_esp32() primero.")

    respuesta = enviar_recibir_datos(esp32_socket, datos)
    return respuesta

# Función para cerrar la conexión con el ESP32
def cerrar_conexion_esp32():
    global esp32_socket
    if esp32_socket is not None:
        cerrar_conexion(esp32_socket)
        esp32_socket = None

# Función principal para enviar datos al ESP32 y recibir una respuesta
def conection(input_data):
    datos_a_enviar = input_data
    respuesta_del_esp32 = enviar_datos_al_esp32(datos_a_enviar)
    print(f"Recibido desde ESP32: {respuesta_del_esp32}")

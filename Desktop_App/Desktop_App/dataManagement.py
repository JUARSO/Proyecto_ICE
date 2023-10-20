import json


"""
    Esta función escribe datos en un archivo JSON que representa una tabla de información.

    Entradas:
    - disntanciaUltrrasonico (str): La distancia ultrasónica a escribir en la tabla.
    - nombreArchivoAudio (str): El nombre del archivo de audio asociado.
    - nombre_archivo (str): El nombre del archivo JSON en el que se escribirán los datos.

    Salidas:
    - Ninguna, ya que esta función escribe datos en el archivo JSON.

    Restricciones:
    - 'nombre_archivo' debe ser una cadena válida que represente el nombre del archivo JSON.
"""
# Manejo de datos - Función para escribir en una tabla

def escribir_json_tabla(disntanciaUltrrasonico, nombreArchivoAudio, nombre_archivo):


    try:
        # Cargar datos existentes desde el archivo JSON
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        datos = []

    Nuevodato = {
        "Distancia Ultrasonico": disntanciaUltrrasonico,
        "Estimacion IA": 'NA',
        "Audio": nombreArchivoAudio
    }

    if len(datos) > 10:
        datos = datos[:1]

    datos.append(Nuevodato)

    # Guardar los datos actualizados en el archivo JSON
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos, archivo, indent=2)

# Manejo de datos - Función para datos de entrenamiento
"""
    Esta función agrega datos de entrenamiento a un archivo JSON.

    Entradas:
    - disntanciaUltrrasonico (str): La distancia ultrasónica a agregar a los datos de entrenamiento.
    - nombreArchivoAudio (str): El nombre del archivo de audio asociado.
    - nombre_archivo (str): El nombre del archivo JSON en el que se agregarán los datos de entrenamiento.

    Salidas:
    - Ninguna, ya que esta función agrega datos de entrenamiento al archivo JSON.

    Restricciones:
    - 'nombre_archivo' debe ser una cadena válida que represente el nombre del archivo JSON.

"""
def datos_de_entrenamiento(disntanciaUltrrasonico, nombreArchivoAudio, nombre_archivo):


    try:
        # Cargar datos existentes desde el archivo JSON
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        datos = []

    Nuevodato = {
        "Distancia Ultrasonico": disntanciaUltrrasonico,
        "Audio": nombreArchivoAudio
    }

    datos.append(Nuevodato)

    # Guardar los datos de entrenamiento en el archivo JSON
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos, archivo, indent=2)
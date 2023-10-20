import tkinter as tk
from tkinter import ttk
import json
import threading
import socket
import os
import sounddevice as sd
import dataManagement
from Audio_Processing  import audio_processing
from scipy.io.wavfile import write

# Variables globales para almacenar los valores
nombre_archivo_global = ""
respuesta_global = ""
tabla = None

def cerrar_ventana():
    ventana.destroy()

#Esta función inicia dos hilos para escuchar sonido y enviar sonido al microcontrolador. 
def iniciar_escucha_y_envio():
    #Crear un hilo para escuchar sonido
    hilo_escucha = threading.Thread(target=escucharSonido)
    # Crear un hilo para enviar sonido al microcontrolador con el comando 'S' y el callback 'callback_actualizar_tabla'
    hilo_envio = threading.Thread(target=lambda: enviar_sonido_al_microcontrolador('S', callback_actualizar_tabla))
    # Iniciar el hilo de envío
    hilo_envio.start()
    # Iniciar el hilo de escucha
    hilo_escucha.start()
    
"""
    Esta función graba un audio durante un tiempo específico y lo guarda en un archivo.

    Entradas:
    - nombre_archivo (str): El nombre del archivo en el que se guardará el audio.
    - duracion_segundos (int): La duración en segundos de la grabación.
    - frecuencia_muestreo (int): La frecuencia de muestreo del audio.

    Restricciones:
    - 'nombre_archivo' debe ser una cadena que represente una ruta de archivo válida.
    - 'duracion_segundos' debe ser un entero mayor que cero.
    - 'frecuencia_muestreo' debe ser un entero que represente la frecuencia de muestreo del audio.
"""
def escucharSonido():
    nombre_archivo = "Red_Neuronal\AudiosEntrenamiento"  # Nombre del archivo de salida
    duracion_segundos = 1  # Duración de la grabación en segundos
    frecuencia_muestreo = 44100  # Frecuencia de muestreo del audio
    grabar_audio(nombre_archivo, duracion_segundos, frecuencia_muestreo)

"""
    Esta función envía un mensaje de sonido al microcontrolador a través de un socket y llama a un callback para actualizar la tabla.

    Entradas:
    - mensaje_sonido (str): El mensaje de sonido que se enviará al microcontrolador.
    - callback (función): La función de callback que se llamará después de recibir la respuesta del microcontrolador.

    Salidas:
    - None: No devuelve ningún valor directamente, pero actualiza la variable global 'respuesta_global' y llama al callback.

    Restricciones:
    - 'mensaje_sonido' debe ser una cadena válida que represente el mensaje de sonido a enviar.
    - 'callback' debe ser una función válida que se llamará después de recibir la respuesta del microcontrolador.

"""

def enviar_sonido_al_microcontrolador(mensaje_sonido, callback):

    global respuesta_global  # Variable global para almacenar la respuesta

    microcontrolador_ip = "192.168.1.100"
    microcontrolador_puerto = 1234

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as microcontrolador_socket:
            microcontrolador_socket.connect((microcontrolador_ip, microcontrolador_puerto))
            microcontrolador_socket.sendall(mensaje_sonido.encode('utf-8'))

            # Recibir la respuesta del microcontrolador
            respuesta = microcontrolador_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del microcontrolador: {respuesta}")

            respuesta_global = respuesta

            # Llamar al callback para actualizar la tabla
            callback()

    except Exception as e:
        print(f"Error al enviar/recibir sonido al/from microcontrolador: {e}")

"""
    Esta función graba audio desde un micrófono, guarda los datos de audio en un archivo WAV y retorna el nombre del archivo.

    Entradas:
    - directorio (str): El directorio en el que se guardará el archivo de audio.
    - duracion_segundos (int): La duración en segundos de la grabación.
    - frecuencia_muestreo (int): La frecuencia de muestreo del audio.

    Salidas:
    - nombre_archivo_global (str): El nombre del archivo WAV en el que se guarda el audio.

    Restricciones:
    - 'directorio' debe ser una cadena válida que represente una ruta de directorio.
    - 'duracion_segundos' debe ser un entero mayor que cero.
    - 'frecuencia_muestreo' debe ser un entero que represente la frecuencia de muestreo del audio.
"""

def grabar_audio(directorio, duracion_segundos, frecuencia_muestreo):

    print("Grabando audio...")

    # Verificar si el directorio existe, si no, crearlo
    if not os.path.exists(directorio):
        os.makedirs(directorio)

    # Cuenta el número de archivos en el directorio
    num_archivos = len([f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))])

    # Generar nombre de archivo único basado en el número de archivos
    global nombre_archivo_global
    nombre_archivo_global = os.path.join(directorio, f"audio_{num_archivos + 1}.wav")

    # Grabar audio desde el micrófono
    audio = sd.rec(int(duracion_segundos * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=2, dtype='int16')
    sd.wait()

    # Guardar datos de audio en un archivo WAV
    write(nombre_archivo_global, frecuencia_muestreo, audio)

    print(f"Audio guardado en '{nombre_archivo_global}'.")

    return nombre_archivo_global

"""
    Esta función actualiza dos tablas de datos: una en el archivo 'dataTable.json' y otra en el archivo 'TrainingData.json'.

    Entradas:
    - nombre_archivo_global (str): El nombre del archivo de audio utilizado en la grabación.
    - respuesta_global (str): La respuesta del microcontrolador, que generalmente representa la distancia ultrasónica.

    Restricciones:
    - 'nombre_archivo_global' debe ser una cadena válida que representa el nombre del archivo de audio.
    - 'respuesta_global' debe ser una cadena que generalmente representa la distancia ultrasónica.

"""


def callback_actualizar_tabla():

    global nombre_archivo_global
    global respuesta_global

    # Actualizar la tabla en el archivo 'dataTable.json'
    dataManagement.escribir_json_tabla(disntanciaUltrrasonico=respuesta_global, nombreArchivoAudio=nombre_archivo_global,
                        nombre_archivo='Desktop_App\Desktop_App\dataTable.json')

    # Actualizar la tabla en el archivo 'TrainingData.json'
    dataManagement.datos_de_entrenamiento(disntanciaUltrrasonico=respuesta_global, nombreArchivoAudio=nombre_archivo_global,
                        nombre_archivo='Red_Neuronal\TrainindData.json')


"""
    Esta función se activa cuando se hace doble clic en una fila de la tabla y muestra información relevante.

    Entradas:
    - event: El evento que activa esta función, generalmente un doble clic en una fila de la tabla.

    Salidas:
    - Ninguna, ya que esta función imprime información en la consola.

    Restricciones:
    - La variable global 'tabla' debe estar definida y debe ser una tabla válida.

"""

def on_doble_clic(event):

    global tabla

    if tabla:
        seleccion = tabla.selection()  # Obtener la selección actual en la tabla
        if seleccion:
            item = seleccion[0]  # Obtener el ítem seleccionado
            valores = tabla.item(item, 'values')  # Obtener los valores de la fila seleccionada
            print("Información de la fila seleccionada:")
            print(f"Distancia Ultrasonico: {valores[0]}")
            print(f"Estimacion IA: {valores[1]}")
            print(f"Audio: {valores[2]}")

            # Llamar a 'audio_processing.main' con parámetros específicos
            audio_processing.main(frecuencia_corte_sup=400, frecuencia_corte_inf=200, ruta_archivo=valores[2])
        else:
            print("No hay fila seleccionada.")
        
    
"""
    Esta función inicializa una tabla en una ventana de la interfaz gráfica.

    Entradas:
    - ventana: La ventana de la interfaz gráfica en la que se colocará la tabla.

    Salidas:
    - tabla: La tabla creada y configurada.

    Restricciones:
    - La variable global 'tabla' debe estar definida para que esta función la actualice.
"""

def inicializar_tabla(ventana):
    global tabla
    tabla_frame = ttk.Frame(ventana, style="Tabla.TFrame")
    tabla_frame.pack(padx=20, pady=20, fill='both', expand=True)

    tabla = ttk.Treeview(tabla_frame, columns=('Distancia Ultrasonico', 'Estimacion IA', 'Audio'), show='headings')

    tabla.heading('Distancia Ultrasonico', text='Distancia Ultrasonico')
    tabla.heading('Estimacion IA', text='Estimacion IA')
    tabla.heading('Audio', text='Audio')

    for col in tabla['columns']:
        tabla.column(col, anchor='center')
    tabla.pack(fill='both', expand=True)
    # Vincular evento de doble clic
    tabla.bind("<Double-1>", on_doble_clic)
    return tabla


"""
    Esta función actualiza una tabla con datos cargados desde un archivo JSON y se llama periódicamente.
    Entradas:
    - tabla: La tabla que se actualizará con los datos.
    Salidas:
    - Ninguna, ya que esta función actualiza la tabla, pero no devuelve ningún valor.
    Restricciones:
    - La variable 'tabla' debe ser una tabla válida en la interfaz gráfica.
"""
def actualizar_tabla(tabla):

    with open("Desktop_App\Desktop_App\dataTable.json", "r", encoding='utf-8') as archivo:
        datos = json.load(archivo)

    # Borrar todas las filas existentes en la tabla
    for i in tabla.get_children():
        tabla.delete(i)

    # Agregar filas con valores del archivo JSON
    for fila in datos:
        tabla.insert('', 'end', values=(fila['Distancia Ultrasonico'], fila['Estimacion IA'], fila['Audio']))

    # Llamar a la función nuevamente después de 1000 milisegundos (1 segundo)
    ventana.after(1000, lambda: actualizar_tabla(tabla))


"""
    Esta función inicia una interfaz gráfica para el sistema 'Batimovil'.

    Restricciones:
    - La función 'iniciar_escucha_y_envio' debe estar definida y funcional para ser llamada al presionar el botón.

"""
def iniciar_interfaz():
    global ventana
    ventana = tk.Tk()
    ventana.title("Batimovil")
    ventana.geometry("1500x800")
    ventana.configure(bg="#C0C0C0")

    modo_actual = tk.StringVar()
    modo_actual.set("N/A")

    estilo = ttk.Style()
    estilo.configure("Tabla.TFrame", background="#E0E0E0")

    generaSonidoB = ttk.Button(ventana, text="Generar Sonido", command=iniciar_escucha_y_envio)
    generaSonidoB.pack(side=tk.TOP, pady=5)

    tabla = inicializar_tabla(ventana)
    actualizar_tabla(tabla)

    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

    ventana.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()

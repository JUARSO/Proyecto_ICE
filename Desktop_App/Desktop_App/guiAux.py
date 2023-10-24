import tkinter as tk
from tkinter import ttk
import time
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
proceso_en_ejecucion = False  # Variable para verificar si un proceso está en ejecución
ejecucion_automatica = False  # Variable para controlar la ejecución automática

def cerrar_ventana():
    ventana.destroy()

def iniciar_escucha_y_envio():
    global proceso_en_ejecucion

    if not proceso_en_ejecucion:
        proceso_en_ejecucion = True

        # Crear un hilo para escuchar sonido
        hilo_escucha = threading.Thread(target=escucharSonido)
        # Crear un hilo para enviar sonido al microcontrolador con el comando 'S' y el callback 'callback_actualizar_tabla'
        hilo_envio = threading.Thread(target=lambda: enviar_sonido_al_microcontrolador('S', callback_actualizar_tabla))
        # Iniciar el hilo de envío
        hilo_envio.start()
        # Iniciar el hilo de escucha
        hilo_escucha.start()
    else:
        print("El proceso anterior aún no ha terminado.")

def escucharSonido():
    nombre_archivo = "Proyecto_ICE\Red_Neuronal\Audios"  # Nombre del archivo de salida
    duracion_segundos = 1  # Duración de la grabación en segundos
    frecuencia_muestreo = 44100  # Frecuencia de muestreo del audio
    grabar_audio(nombre_archivo, duracion_segundos, frecuencia_muestreo)

def enviar_sonido_al_microcontrolador(mensaje_sonido, callback):
    global respuesta_global  # Variable global para almacenar la respuesta
    microcontrolador_ip = "192.168.1.100"
    microcontrolador_puerto = 1234
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as microcontrolador_socket:
            microcontrolador_socket.connect((microcontrolador_ip, microcontrolador_puerto))
            microcontrolador_socket.sendall(mensaje_sonido.encode('utf-8'))
            respuesta = microcontrolador_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del microcontrolador: {respuesta}")
            respuesta_global = respuesta
            callback()
    except Exception as e:
        print(f"Error al enviar/recibir sonido al/from microcontrolador: {e}")

def grabar_audio(directorio, duracion_segundos, frecuencia_muestreo):
    print("Grabando audio...")
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    num_archivos = len([f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))])
    global nombre_archivo_global
    nombre_archivo_global = os.path.join(directorio, f"audio_{num_archivos + 1}.wav")
    audio = sd.rec(int(duracion_segundos * frecuencia_muestreo), 
                   samplerate=frecuencia_muestreo, channels=2, dtype='int16')
    sd.wait()
    write(nombre_archivo_global, frecuencia_muestreo, audio)
    print(f"Audio guardado en '{nombre_archivo_global}'.")
    return nombre_archivo_global

def callback_actualizar_tabla():
    global nombre_archivo_global
    global respuesta_global
    dataManagement.escribir_json_tabla(disntanciaUltrrasonico=respuesta_global, nombreArchivoAudio=nombre_archivo_global,
                        nombre_archivo='Proyecto_ICE\Desktop_App\Desktop_App\dataTable.json')
    dataManagement.datos_de_entrenamiento(disntanciaUltrrasonico=respuesta_global, nombreArchivoAudio=nombre_archivo_global,
                        nombre_archivo='Proyecto_ICE\Red_Neuronal\TrainindData.json')
    global proceso_en_ejecucion 
    proceso_en_ejecucion = False

def on_doble_clic(event):
    global tabla
    if tabla:
        seleccion = tabla.selection()
        if seleccion:
            item = seleccion[0]
            valores = tabla.item(item, 'values')
            print("Información de la fila seleccionada:")
            print(f"Distancia Ultrasonico: {valores[0]}")
            print(f"Estimacion IA: {valores[1]}")
            print(f"Audio: {valores[2]}")
            audio_processing.main(frecuencia_corte_sup=400, frecuencia_corte_inf=200, ruta_archivo=valores[2])
        else:
            print("No hay fila seleccionada.")

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
    tabla.bind("<Double-1>", on_doble_clic)
    return tabla

def actualizar_tabla(tabla):
    with open("Proyecto_ICE\Desktop_App\Desktop_App\dataTable.json", "r", encoding='utf-8') as archivo:
        datos = json.load(archivo)
    for i in tabla.get_children():
        tabla.delete(i)
    for fila in datos:
        tabla.insert('', 'end', values=(fila['Distancia Ultrasonico'], fila['Estimacion IA'], fila['Audio']))
    ventana.after(1000, lambda: actualizar_tabla(tabla))

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
    iniciar_auto_button = ttk.Button(ventana, text="Iniciar Escucha y Envío Automático", command=iniciar_escucha_envio_automatico)
    iniciar_auto_button.pack(side=tk.TOP, pady=5)
    detener_auto_button = ttk.Button(ventana, text="Detener Escucha y Envío Automático", command=detener_escucha_envio_automatico)
    detener_auto_button.pack(side=tk.TOP, pady=5)
    tabla = inicializar_tabla(ventana)
    actualizar_tabla(tabla)
    ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)
    ventana.mainloop()

def iniciar_escucha_envio_automatico():
    global ejecucion_automatica
    if not ejecucion_automatica:
        ejecucion_automatica = True
        num_iteraciones = 700
          # Define el número de iteraciones que deseas realizar

        for i in range(num_iteraciones):
            if not ejecucion_automatica:
                break  # Si se detiene la ejecución automática, sal del bucle

            print(f'Iniciando iteración {i + 1}')
            iniciar_escucha_y_envio()  # Llama a la función de escucha y envío
            time.sleep(2)  # Espera 5 segundos entre iteraciones

        ejecucion_automatica = False  # Restablece la variable de control al final

def detener_escucha_envio_automatico():
    global ejecucion_automatica
    ejecucion_automatica = False  # Detiene la ejecución automática

if __name__ == "__main__":
    iniciar_interfaz()

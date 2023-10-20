import numpy as np
import wave

# Función para generar una señal multifrecuencia
def generar_senal_multifrecuencia(frecuencias, duracion, tasa_muestreo=44100, amplitud=0.5):
    tiempo = np.arange(0, duración, 1/tasa_muestreo)
    senal = np.zeros_like(tiempo)

    for frecuencia in frecuencias:
        senal += amplitud * np.sin(2 * np.pi * frecuencia * tiempo)

    return senal

# Función para guardar una señal como archivo WAV
def guardar_wav(nombre_archivo, senal, tasa_muestreo=44100):
    objeto_wave = wave.open(nombre_archivo, 'w')
    objeto_wave.setnchannels(1)  # 1 canal (mono)
    objeto_wave.setsampwidth(2)  # 2 bytes por muestra
    objeto_wave.setframerate(tasa_muestreo)
    objeto_wave.writeframes((senal * 32767).astype(np.int16).tobytes())
    objeto_wave.close()

if __name__ == "__main__":
    # Frecuencias de las ondas senoidales
    frecuencias = [103, 880, 1320, 2032, 13]  # Puedes agregar más frecuencias según sea necesario

    # Parámetros generales
    duracion = 3  # Duración en segundos

    # Generar señal multifrecuencia
    senal_multifrecuencia = generar_senal_multifrecuencia(frecuencias, duracion)

    # Guardar como archivo WAV
    nombre_archivo = "senal_multifrecuencia.wav"
    guardar_wav(nombre_archivo, senal_multifrecuencia)

    print(f"Archivo {nombre_archivo} generado exitosamente.")

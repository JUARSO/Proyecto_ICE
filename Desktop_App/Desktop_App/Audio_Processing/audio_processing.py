import numpy as np  # Importa la biblioteca NumPy con el alias np para facilitar su uso
import matplotlib.pyplot as plt  # Importa la sub-biblioteca pyplot de Matplotlib con el alias plt
from scipy.io import wavfile  # Importa la función wavfile de la biblioteca SciPy para leer archivos de audio WAV
from scipy.signal import butter, lfilter  # Importa las funciones butter y lfilter de la biblioteca SciPy para el diseño y la aplicación de filtros

def leer_archivo_audio(ruta_archivo):
    """Lee un archivo de audio y devuelve la frecuencia de muestreo y los datos de la señal."""
    frecuencia_muestreo, datos = wavfile.read(ruta_archivo)  # Lee el archivo de audio y obtiene la frecuencia de muestreo y los datos de la señal
    return frecuencia_muestreo, datos  # Devuelve la frecuencia de muestreo y los datos de la señal

def graficar_senal(tiempo, senal, titulo, etiqueta_x, etiqueta_y):
    """Grafica una señal en el dominio del tiempo."""
    plt.figure()  # Crea una nueva figura
    plt.plot(tiempo, senal)  # Grafica la señal en función del tiempo
    plt.title(titulo)  # Establece el título de la gráfica
    plt.xlabel(etiqueta_x)  # Etiqueta el eje x
    plt.ylabel(etiqueta_y)  # Etiqueta el eje y
    plt.grid(True)  # Muestra una cuadrícula en la gráfica
    plt.show()  # Muestra la gráfica

def graficar_espectro_frecuencia(senal, frecuencia_muestreo, titulo, etiqueta_x, etiqueta_y):
    """Grafica el espectro de frecuencia de una señal."""
    n = len(senal)  # Obtiene la longitud de la señal
    k = np.arange(n)  # Crea un vector k desde 0 hasta n-1
    t = n / frecuencia_muestreo  # Calcula el tiempo total de la señal
    frq = k / t  # Calcula el vector de frecuencias
    frq = frq[range(n//2)]  # Selecciona la mitad de las frecuencias (debido a la simetría)

    transformada = np.fft.fft(senal) / n  # Calcula la transformada de Fourier y normaliza
    transformada = transformada[range(n//2)]  # Selecciona la mitad de la transformada

    plt.figure()  # Crea una nueva figura
    plt.plot(frq, abs(transformada))  # Grafica el espectro de frecuencia
    plt.title(titulo)  # Establece el título de la gráfica
    plt.xlabel(etiqueta_x)  # Etiqueta el eje x
    plt.ylabel(etiqueta_y)  # Etiqueta el eje y
    plt.grid(True)  # Muestra una cuadrícula en la gráfica
    plt.show()  # Muestra la gráfica

def filtro_pasabanda(senal, frecuencia_muestreo, frecuencia_corte_inf, frecuencia_corte_sup, orden=4):
    """Aplica un filtro pasabanda a una señal."""
    nyquist = 0.5 * frecuencia_muestreo  # Frecuencia de Nyquist
    normal_frec_corte_inf = frecuencia_corte_inf / nyquist  # Frecuencia de corte inferior normalizada
    normal_frec_corte_sup = frecuencia_corte_sup / nyquist  # Frecuencia de corte superior normalizada

    # Diseño del filtro
    b, a = butter(orden, [normal_frec_corte_inf, normal_frec_corte_sup], btype='band')

    # Aplicar filtro
    senal_filtrada = lfilter(b, a, senal)
    
    return senal_filtrada

def main(ruta_archivo, frecuencia_corte_inf, frecuencia_corte_sup):
    # Leer archivo de audio
    frecuencia_muestreo, datos_audio = leer_archivo_audio(ruta_archivo)

    # Crear vector de tiempo
    tiempo = np.arange(0, len(datos_audio)) / frecuencia_muestreo

    # Graficar señal original en el dominio del tiempo
    graficar_senal(tiempo, datos_audio, 'Señal Original en el Tiempo', 'Tiempo (s)', 'Amplitud')

    # Graficar espectro de frecuencia de la señal original
    graficar_espectro_frecuencia(datos_audio, frecuencia_muestreo, 'Espectro de Frecuencia de la Señal Original', 'Frecuencia (Hz)', 'Amplitud')

    # Aplicar filtro pasabanda
    senal_filtrada = filtro_pasabanda(datos_audio, frecuencia_muestreo, frecuencia_corte_inf, frecuencia_corte_sup)

    # Graficar señal filtrada en el dominio del tiempo
    graficar_senal(tiempo, senal_filtrada, 'Señal Filtrada en el Tiempo', 'Tiempo (s)', 'Amplitud')

    # Graficar espectro de frecuencia de la señal filtrada
    graficar_espectro_frecuencia(senal_filtrada, frecuencia_muestreo, 'Espectro de Frecuencia de la Señal Filtrada', 'Frecuencia (Hz)', 'Amplitud')

if __name__ == "__main__":
    # Ruta del archivo de audio
    ruta_archivo = 'grabacion.wav'
    
    # Frecuencias de corte del filtro pasabanda
    frecuencia_corte_inf = 800
    frecuencia_corte_sup = 1200

    # Llamar a la función main con los argumentos especificados
    main(ruta_archivo, frecuencia_corte_inf, frecuencia_corte_sup)

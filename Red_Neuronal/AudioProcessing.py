import os
import json
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
def HistogramaDeDatos():
    with open('Proyecto_ICE\Red_Neuronal\TrainindData.json', 'r') as json_file:
        data = json.load(json_file)

    # Filtra las distancias para mantener solo aquellas menores o iguales a 200 cm
    distancias = [int(item["Distancia Ultrasonico"]) for item in data if int(item["Distancia Ultrasonico"]) <= 200]

    # Crea un histograma con intervalos de 10 cm
    plt.hist(distancias, bins=range(0, 201, 10), edgecolor='black')
    plt.xlabel('Distancia (cm)')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Distancias Ultrasónicas (menores o iguales a 200 cm)')
    plt.grid(True)
    plt.show()

HistogramaDeDatos()
def EspectrogramadeAudio():
    # Carga la señal de audio
    audio_file = 'Proyecto_ICE\\Red_Neuronal\\Audios\\audio_4.wav'
    y, sr = librosa.load(audio_file)

    # Calcula el espectrograma usando la transformada rápida de Fourier (FFT)
    D = np.abs(librosa.stft(y))

    # Convierte el espectrograma a decibeles (escala logarítmica)
    D_db = librosa.amplitude_to_db(D, ref=np.max)

    # Visualiza el espectrograma
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(D_db, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Espectrograma de la señal de audio')
    plt.show()

def graficarSeñalFurier():
    # Cargar el archivo de audio
    audio_file = 'Proyecto_ICE\\Red_Neuronal\\Audios\\audio_4.wav'
    y, sr = librosa.load(audio_file)

    # Calcular la transformada de Fourier
    fft_result = np.fft.fft(y)
    N = len(fft_result)
    frequencies = np.fft.fftfreq(N, 1/sr)

    # Tomar solo las componentes de frecuencia positiva
    positive_frequencies = frequencies[:N//2]
    positive_fft_result = np.abs(fft_result[:N//2])

    # Graficar la magnitud de la transformada de Fourier (parte positiva)
    plt.figure(figsize=(10, 6))
    plt.plot(positive_frequencies, positive_fft_result)
    plt.title('Transformada de Fourier de la señal de audio (parte positiva)')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Amplitud')
    plt.grid()
    plt.show()


import librosa
import numpy as np
import json
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
#27.170675037312805 cm
# 1. Parsear el conjunto de datos
def parse_json_dataset(json_file, max_distance=200):
    X = []  # Almacenaremos los espectrogramas
    y = []  # Almacenaremos las distancias ultrasónicas

    with open(json_file, 'r') as file:
        data = json.load(file)

    for entry in data:
        audio_path = entry["Audio"]
        distance_ultrasonic = float(entry["Distancia Ultrasonico"])

        if distance_ultrasonic <= max_distance:
            print(f"[+] Parsing {audio_path}...")

            # Cargar el archivo de audio y calcular el espectrograma
            wav, _ = librosa.load(audio_path, sr=None)
            spectrogram = librosa.feature.melspectrogram(y=wav, sr=_)

            # Normalizar el espectrograma (opcional)
            spectrogram = np.log1p(spectrogram)

            # Agregar una dimensión de canal (1) a los espectrogramas
            spectrogram = np.expand_dims(spectrogram, axis=-1)

            X.append(spectrogram)
            y.append(distance_ultrasonic)

    return X, y


json_file = 'Proyecto_ICE\\Red_Neuronal\\TrainindData.json'
X, y = parse_json_dataset(json_file)

# 2. Dividir los datos en conjuntos de entrenamiento y prueba (95% entrenamiento, 5% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.02, random_state=42)

# 3. Construir el modelo CNN
model = keras.Sequential([
    keras.layers.Input(shape=X_train[0].shape),
    keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)  # Capa de salida para la distancia
])


# 4. Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')  # Puedes cambiar la función de pérdida según tu preferencia

# 5. Configurar TensorBoard para el registro
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="logs")

# 6. Entrenar el modelo
model.fit(np.array(X_train), np.array(y_train), epochs=10, batch_size=32, validation_data=(np.array(X_test), np.array(y_test)), callbacks=[tensorboard_callback])

# 7. Realizar predicciones en el conjunto de prueba
y_pred = model.predict(np.array(X_test))

# 8. Evaluar el rendimiento del modelo
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error en el conjunto de prueba: {mae} cm")

import librosa
import numpy as np
import json
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
# 23.170675037312805 cm
# 1. Parsear el conjunto de datos
def parse_json_dataset(json_file, max_distance=400):
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

# 3. Definir la función de pérdida personalizada para limitar el error a ±5 cm
def custom_huber_loss(y_true, y_pred):
    error = y_true - y_pred
    is_small_error = tf.abs(error) <= 5.0
    small_error_loss = tf.square(error) / 2
    large_error_loss = 5.0 * (tf.abs(error) - 2.5)
    return tf.where(is_small_error, small_error_loss, large_error_loss)

# 4. Construir el modelo CNN (modelo más profundo)
model = keras.Sequential([
    keras.layers.Input(shape=X_train[0].shape),
    keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu'),
    keras.layers.MaxPooling2D(pool_size=(2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(1)  # Capa de salida para la distancia
])

# 5. Compilar el modelo con la función de pérdida personalizada
model.compile(optimizer='adam', loss=custom_huber_loss)

# 6. Configurar TensorBoard para el registro
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="logs")

# 7. Entrenar el modelo
model.fit(np.array(X_train), np.array(y_train), epochs=10, batch_size=32, validation_data=(np.array(X_test), np.array(y_test)), callbacks=[tensorboard_callback])

# 8. Realizar predicciones en el conjunto de prueba
y_pred = model.predict(np.array(X_test))

# 9. Evaluar el rendimiento del modelo (MAE y MSE)
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error en el conjunto de prueba: {mae} cm")

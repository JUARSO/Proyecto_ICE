#include <ESP8266WiFi.h>
#include <Servo.h>

// Definición de pines
#define PIN_BOCINA D2
#define TRIG_PIN D5
#define ECHO_PIN D6

// Creación de objeto servo y definición de pin
Servo miServo;  
int pinServo = D1;  

// Configuración de direcciones IP estáticas
IPAddress localIP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

// Configuración de servidor y cliente WiFi
WiFiServer server(1234);
WiFiClient client;

// Variables para seguimiento de tiempo y período de inactividad
unsigned long lastActivityTime = 0;
const unsigned long timeoutPeriod = 120000;

void setup() {
    Serial.begin(115200);

    // Conexión a Wi-Fi con dirección IP estática
    WiFi.config(localIP, gateway, subnet);
    const char* ssid = "SOLIS ARGUELLO 2";
    const char* password = "2pa25472";
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Conectando a Wi-Fi...");
    }

    server.begin();
    Serial.println("Servidor listo");

    // Configuración de pines para el sensor ultrasónico y la bocina
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(PIN_BOCINA, OUTPUT);
}

void loop() {
    if (!client.connected()) {
        if (server.hasClient()) {
            if (client) {
                client.stop(); // Si hay un cliente existente, ciérralo
            }
            client = server.available();
            lastActivityTime = millis(); // Reinicia el temporizador de actividad
        }
    } else {
        if (client.available()) {
            char request = client.read();

            if (request == 'S') {
                // Realiza la medición de distancia y envía la información al cliente
                distanciaUltraSonicos();
            }

            // Aquí no necesitas enviar "Respuesta desde ESP8266!" ya que enviarás la distancia en la función distanciaUltraSonicos
        }

        // Verifica si ha pasado el período de tiempo sin actividad y desconecta al cliente
        if (millis() - lastActivityTime > timeoutPeriod) {
            client.stop();
            Serial.println("Cliente desconectado debido a inactividad.");
        }
    }
}

void distanciaUltraSonicos() {
    // Emite un pulso ultrasónico
    miServo.attach(pinServo);  
    miServo.write(90); 

    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    // Mide el tiempo que tarda en llegar el eco
    long duration = pulseIn(ECHO_PIN, HIGH);

    // Calcula la distancia en centímetros
    int distance = duration * 0.034 / 2;

    // Muestra la distancia en el puerto serie
    Serial.print("Distancia: ");
    Serial.print(distance);
    Serial.println(" cm");

    // Envía la distancia al cliente
    client.print(distance);

    // Produce un tono en la bocina
    tone(PIN_BOCINA, 300);
    delay(1000);
    noTone(PIN_BOCINA);

    // Espera antes de realizar la próxima medición
    delay(500);

    // Actualiza el tiempo de la última actividad
    lastActivityTime = millis();
}

#include <WiFi.h>

#define PIN_BOCINA_1 32
#define PIN_BOCINA_2 27

IPAddress localIP(192, 168, 1, 100);  // Configura la dirección IP del ESP32
IPAddress gateway(192, 168, 1, 1);    // Configura la dirección IP del gateway
IPAddress subnet(255, 255, 255, 0);   // Configura la máscara de subred

WiFiServer server(1234);
WiFiClient client;

unsigned long lastActivityTime = 0;
const unsigned long timeoutPeriod = 120000;  // Timeout después de 2 minutos de inactividad

void setup() {
    Serial.begin(115200);

    // Conéctate a Wi-Fi con dirección IP estática
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
}

void loop() {
    if (!client.connected()) {
        client = server.available();
        if (client) {
            Serial.println("Nuevo cliente conectado.");
            lastActivityTime = millis();  // Reinicia el temporizador cuando se conecta un nuevo cliente
        }
    } else {
        if (client.available()) {
            char request = client.read();
            //Serial.write(request);

            // Hacer algo con los datos recibidos si es necesario
            if(request == 'S'){
              sonar();
            }

            // Enviar una respuesta de vuelta al cliente
            client.print("Respuesta desde ESP32!");

            lastActivityTime = millis();  // Reinicia el temporizador cuando se recibe un dato
        }
    }

    // Comprobar el tiempo de inactividad
    if (millis() - lastActivityTime > timeoutPeriod) {
        Serial.println("Tiempo de inactividad excedido. Cerrando la conexión.");
        client.stop();
    }
}

void sonar(){
    // Lee el valor analógico del pin A0
    // Configurar los pines como salidas
  pinMode(PIN_BOCINA_1, OUTPUT);
  pinMode(PIN_BOCINA_2, OUTPUT);
  
  // Iniciar la generación de tono en ambos pines
  tone(PIN_BOCINA_1, 600);  // 600 Hz en el pin 32
  tone(PIN_BOCINA_2, 600);  // 600 Hz en el pin 27

  // Pausar durante 1 segundo
  delay(1000);

  // Detener la generación de tono en ambos pines
  noTone(PIN_BOCINA_1);
  noTone(PIN_BOCINA_2);
}



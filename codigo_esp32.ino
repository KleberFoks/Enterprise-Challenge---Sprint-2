#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// Configuração do DHT22
#define DHTPIN 4
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// Configuração Wi-Fi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Configuração MQTT
const char* mqttServer = "broker.hivemq.com";
const int mqttPort = 1883;
const char* mqttTopic = "esp32/flood/temperature_humidity";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Conecta no Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Wi-Fi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Configura servidor MQTT
  client.setServer(mqttServer, mqttPort);

  // Conecta no MQTT
  Serial.print("Conectando ao MQTT...");
  while (!client.connected()) {
    if (client.connect("ESP32ClientDHT")) {
      Serial.println("Conectado ao broker MQTT!");
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(". Tentando novamente em 2 segundos...");
      delay(2000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    // Tenta reconectar ao MQTT se perdeu conexão
    while (!client.connected()) {
      Serial.print("Reconectando ao MQTT...");
      if (client.connect("ESP32ClientDHT")) {
        Serial.println("Reconectado!");
      } else {
        Serial.print("Falhou, rc=");
        Serial.print(client.state());
        Serial.println(". Tentando novamente em 2 segundos...");
        delay(2000);
      }
    }
  }
  client.loop();

  // Leitura do sensor DHT22
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Falha ao ler do sensor DHT22!");
    delay(2000);
    return;
  }

  // Formata dados para envio MQTT: "temp:24.5,hum:55.8"
  char payload[50];
  snprintf(payload, sizeof(payload), "temp:%.1f,hum:%.1f", temperature, humidity);

  Serial.print("Publicando: ");
  Serial.println(payload);

  client.publish(mqttTopic, payload);

  delay(3000); // espera 5 segundos antes da próxima leitura e publicação
}

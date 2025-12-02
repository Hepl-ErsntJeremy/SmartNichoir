#include "M5TimerCAM.h"
#include <WiFi.h>
#include <PubSubClient.h>

#define WIFI_SSID     "electroProjectWifi"
#define WIFI_PASS     "B1MesureEnv"

#define MQTT_SERVER   "192.168.2.41"   // Raspberry Pi IP
#define MQTT_PORT     1883  

WiFiClient espClient;
PubSubClient client(espClient);

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connexion MQTT...");
    if (client.connect("TimerCAM", "timercam","12345678" )) {
      Serial.println(" OK");
    } else {
      Serial.print(" Échec : ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  TimerCAM.begin();
  if (!TimerCAM.Camera.begin()) {
    Serial.println("Camera Init Fail");
    return;
  }
  Serial.println("Camera Init Success");
  TimerCAM.Camera.sensor->set_pixformat(TimerCAM.Camera.sensor, PIXFORMAT_JPEG);
  TimerCAM.Camera.sensor->set_framesize(TimerCAM.Camera.sensor, FRAMESIZE_VGA); // 640x480  TimerCAM.Camera.sensor->set_vflip(TimerCAM.Camera.sensor, 1);
  TimerCAM.Camera.sensor->set_hmirror(TimerCAM.Camera.sensor, 0);

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connexion WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connecté !");
  Serial.print("IP TimerCAM : ");
  Serial.println(WiFi.localIP());

  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setBufferSize(40000);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  if (TimerCAM.Camera.get()) {
    Serial.println("Photo !");
    int len = TimerCAM.Camera.fb->len;
    uint8_t* buf = TimerCAM.Camera.fb->buf;

    Serial.println();
    client.publish("camera/photo",buf,len);

    Serial.println("Photo envoyée au Raspberry.");
    
    TimerCAM.Camera.free();
  }

  delay(10000); // 10 secondes
}

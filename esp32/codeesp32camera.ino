#include "M5TimerCAM.h"
#include <PubSubClient.h>
#include <WiFiManager.h>

#define MQTT_SERVER   "192.168.2.223"   // Raspberry Pi IP
#define MQTT_PORT     1883  

#define PIR_PIN 4 //wake up Pin
#define LEDIR_PIN 13 //Infrared LED  Pin 

WiFiClient espClient;
PubSubClient client(espClient);

void connectMQTT() {
  while (!client.connected()) {
    Serial.print("MQTT connected...");
    if (client.connect("TimerCAM", "timercam","12345678" )) {
      Serial.println(" OK");
    } else {
      Serial.print(" Fail : ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void GoToSleep1min (){
  Serial.println(" Sleep 1min...");
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIR_PIN, 1);
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}
 
void GoToSleep24h() {
  Serial.println("Sleep 24h...");
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIR_PIN, 1);
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);// change to 24ULL * 60ULL * 60ULL * 1000000ULL for 24h 
  esp_deep_sleep_start();
}

void BatteryLevel(){
  if (!client.connected()) {
        connectMQTT();
    }
    float level = TimerCAM.Power.getBatteryLevel();
    level = 49.3;
    char msg[50];
    sprintf(msg, "%.2f", level);
    client.publish("camera/battery", msg);
    delay(100);
    Serial.printf("Battery : %s %\n", msg);
}

void setup() {
  Serial.begin(115200);
  TimerCAM.begin(true);
  pinMode(LEDIR_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);

  digitalWrite(LEDIR_PIN, LOW);

  //------------ Connexion Wifi ------------
  WiFiManager wm;
  // Custom parameters
  WiFiManagerParameter custom_api_key("api", "API Key", "", 32);
  WiFiManagerParameter custom_mode("mode", "Device Mode", "", 16);
  wm.addParameter(&custom_api_key);
  wm.addParameter(&custom_mode);

  wm.setConfigPortalTimeout(180); // 3min to config 
  wm.setConnectTimeout(30);       // 30sec to connect

  // Connexion
  if(!wm.autoConnect("ESP32_SmartNichoir_TTPCBB", "12345678")) {
      Serial.println("Wifi connection failed");
  }
  // Get wake-up cause 
  esp_sleep_wakeup_cause_t cause = esp_sleep_get_wakeup_cause();

  //------------ WAKE UP PIR ------------
  if (cause == ESP_SLEEP_WAKEUP_EXT0) {

    Serial.println("Wake Up!");

    // Enable led
    digitalWrite(LEDIR_PIN, HIGH);  
    delay(200);

    // Init camera 
    TimerCAM.begin();  
    if (!TimerCAM.Camera.begin()) {
      Serial.println("Camera Init Fail");
      return;
    }
    Serial.println("Camera Init Success");
    TimerCAM.Camera.sensor->set_pixformat(TimerCAM.Camera.sensor, PIXFORMAT_JPEG);
    TimerCAM.Camera.sensor->set_framesize(TimerCAM.Camera.sensor, FRAMESIZE_VGA); // 640x480  
    TimerCAM.Camera.sensor->set_hmirror(TimerCAM.Camera.sensor, 0);
    TimerCAM.Camera.sensor->set_vflip(TimerCAM.Camera.sensor, 1);

    client.setServer(MQTT_SERVER, MQTT_PORT);
    client.setBufferSize(40000);

    if (TimerCAM.Camera.get()) {
    Serial.println("Photo !");
    int len = TimerCAM.Camera.fb->len;
    uint8_t* buf = TimerCAM.Camera.fb->buf;

    Serial.println();
    client.publish("camera/photo",buf,len);
    Serial.println("Photo sent to Raspberry.");
    BatteryLevel();
    TimerCAM.Camera.free();
    delay(50);
    }
    digitalWrite(LEDIR_PIN, LOW);
    GoToSleep1min();
  }

  //------------ WAKE UP TIMER ------------
  if (cause == ESP_SLEEP_WAKEUP_TIMER) {
    Serial.println(" TIMER WAKE UP!");

    client.setServer(MQTT_SERVER, MQTT_PORT);
    client.setBufferSize(40000); 
    connectMQTT();

    // Publie le log
    if(client.publish("camera/log", "Timer wakeup OK")) {
      delay(100);
      Serial.println("Log sent successfully!");
    } 
    else {
      Serial.println("Failed to send log");
    }
    BatteryLevel();
    client.loop(); // forcer l’envoi immédiat

    // Retour en deep sleep pour 24h
    GoToSleep24h();
  }
  
  // ------------ FIRST BOOT --------------
  Serial.println("First boot => Going to 24h sleep");
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIR_PIN, 1);   // HIGH = wakeup
  GoToSleep24h();
}
void loop(){
}

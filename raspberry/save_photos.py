import paho.mqtt.client as mqtt
from datetime import datetime
import os

SAVE_DIR = "/home/ethan/camera/photos"
os.makedirs(SAVE_DIR, exist_ok=True)

def on_connect(client, userdata, flags, rc):
    print("Connecté MQTT, code:", rc)
    client.subscribe("camera/photo")

def on_message(client, userdata, msg):
    print("Photo reçue !")

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(msg.payload)

    print("Photo enregistrée :", filepath)

client = mqtt.Client()
client.username_pw_set("timercam","12345678")
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.41", 1883, 60)
client.loop_forever()
import paho.mqtt.client as mqtt
from datetime import datetime
import os

from SQLAlchemy import create_engine
from SQLAlchemy.orm import sessionmaker

from SmartNichoir_tables import Photo, Log, Battery, Base

# ----------  MariaDB ----------
engine = create_engine(
    "mariadb+mariadbconnector://ethan:12345678@192.168.2.223:3306/SmartNichoir",
    echo=False
)
Session = sessionmaker(bind=engine)

SAVE_DIR = "/home/ethan/camera/photos"
os.makedirs(SAVE_DIR, exist_ok=True)

def on_connect(client, userdata, flags, rc):
    print("Connecté MQTT, code:", rc)
    client.subscribe("camera/photo")
    client.subscribe("camera/battery")

def on_message(client, userdata, msg):
    # Gérer la batterie
    if msg.topic == "camera/battery":
        try:
            battery_percentage = float(msg.payload.decode())
            with Session() as session:
                new_battery = Battery(
                    percentage=battery_percentage,
                    timestamp=datetime.now()
                )
                session.add(new_battery)
                session.commit()
                print(f"Batterie enregistrée : {battery_percentage}% - ID = {new_battery.id}")
        except Exception as e:
            print("Erreur DB (batterie) :", e)
    
    # Gérer la photo
    elif msg.topic == "camera/photo":
        print("Photo reçue !")

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
        filepath = os.path.join(SAVE_DIR, filename)

        # Enregistrer le fichier localement
        with open(filepath, "wb") as f:
            f.write(msg.payload)

        # Enregistrer dans MariaDB
        try:
            with Session() as session:
                new_photo = Photo(
                    file_name=filename,
                    file_path=filepath,
                    timestamp=datetime.now()
                )
                session.add(new_photo)
                session.commit()
                print("Photo enregistrée dans SQL ! ID =", new_photo.id)

        except Exception as e:
            print("Erreur DB :", e)

        print("Photo enregistrée :", filepath)

client = mqtt.Client()
client.username_pw_set("timercam", "12345678")
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.223", 1883, 60)
client.loop_forever()

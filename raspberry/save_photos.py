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
    client.subscribe("camera/log")  

def on_message(client, userdata, msg):
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
                print(f"Battery : {battery_percentage}% - ID = {new_battery.id}")
        except Exception as e:
            print("DB Error (battery) :", e)

    elif msg.topic == "camera/photo":
        print("Photo received !")

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
        filepath = os.path.join(SAVE_DIR, filename)

        # save file locally
        with open(filepath, "wb") as f:
            f.write(msg.payload)

        # save to database
        try:
            with Session() as session:
                new_photo = Photo(
                    file_name=filename,
                    file_path=filepath,
                    timestamp=datetime.now()
                )
                session.add(new_photo)
                session.commit()
                print("Photo saved ({filepath}) ID =", new_photo.id)

        except Exception as e:
            print("DB Error (photo) :", e)

        print("Photo saved :", filepath)

    elif msg.topic == "camera/log":
        log_message = msg.payload.decode()
        try:
            with Session() as session:
                new_log = Log(
                    message=log_message,
                    timestamp=datetime.now()
                )
                session.add(new_log)
                session.commit()
                print("Log saved ! ID =", new_log.id)
        except Exception as e:
            print("DB Error (log) :", e)

client = mqtt.Client()
client.username_pw_set("timercam", "12345678")
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.223", 1883, 60)
client.loop_forever()

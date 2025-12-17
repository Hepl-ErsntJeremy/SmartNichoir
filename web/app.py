from flask import Flask, render_template
from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import Session

from models import Photo, Battery, Log

app = Flask(__name__)

engine = create_engine(
    "mysql+mysqldb://jeremy:12345678@192.168.2.223:3306/SmartNichoir",
    echo=False
)

@app.route("/")
def index():
    with Session(engine) as session:
        photos = session.scalars(
            select(Photo).order_by(desc(Photo.timestamp))
        ).all()

        last_battery = session.scalars(
            select(Battery).order_by(desc(Battery.timestamp))
        ).first()

        last_logs = session.scalars(
            select(Log).order_by(desc(Log.timestamp)).limit(5)
        ).all()

    return render_template(
        "index.html",
        photos=photos,
        last_battery=last_battery,
        logs=last_logs
    )

@app.route("/log")
def log():
    with Session(engine) as session:
        logs = session.scalars(
            select(Log).order_by(desc(Log.timestamp))
        ).all()

        battery_logs = session.scalars(
            select(Battery).order_by(desc(Battery.timestamp))
        ).all()

    return render_template(
        "log.html",
        logs=logs,
        battery_logs=battery_logs
    )


if __name__ == "__main__":
    app.run(host="192.168.2.223", port=5001, debug=True)

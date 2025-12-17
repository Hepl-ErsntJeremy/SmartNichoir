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

        all_logs = session.scalars(
            select(Log).order_by(desc(Log.timestamp))
        ).all()

        error_logs = []
        warning_logs = []
        info_logs = []

        for log in all_logs:
            msg = log.message.lower()
            if "error" in msg and len(error_logs) < 2:
                error_logs.append(log)
            elif "warning" in msg and len(warning_logs) < 2:
                warning_logs.append(log)
            elif "error" not in msg and "warning" not in msg and len(info_logs) < 2:
                info_logs.append(log)

            if len(error_logs) == 2 and len(warning_logs) == 2 and len(info_logs) == 2:
                break


    return render_template(
        "index.html",
        photos=photos,
        last_battery=last_battery,
        error_logs=error_logs,
        warning_logs=warning_logs,
        info_logs=info_logs
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

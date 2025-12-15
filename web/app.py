from flask import Flask, render_template
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models import Photo

app = Flask(__name__)

engine = create_engine(
    "mysql+mysqldb://jeremy:12345678@192.168.2.223:3306/SmartNichoir",
    echo=False
)

@app.route("/")
def index():
    with Session(engine) as session:
        photos = session.scalars(
            select(Photo).order_by(Photo.timestamp.desc())
        ).all()

    return render_template("index.html", photos=photos)

if __name__ == "__main__":
    app.run(host="192.168.2.223", port=5001, debug=True)
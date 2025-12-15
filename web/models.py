from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, Float, DateTime

# Base pour SQLAlchemy
class Base(DeclarativeBase):
    pass

# --- TABLE PHOTO ---
class Photo(Base):
    __tablename__ = "photos"

    id = mapped_column(Integer, primary_key=True)
    file_name = mapped_column(String(255), nullable=False)
    file_path = mapped_column(String(255), nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)  # date + time

    def __repr__(self):
        return f"<Photo(id={self.id}, file_name='{self.file_name}', timestamp={self.timestamp})>"

# --- TABLE LOG ---
class Log(Base):
    __tablename__ = "logs"

    id = mapped_column(Integer, primary_key=True)
    message = mapped_column(String(255), nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Log(id={self.id}, message='{self.message}', timestamp={self.timestamp})>"

# --- TABLE BATTERY ---
class Battery(Base):
    __tablename__ = "battery"

    id = mapped_column(Integer, primary_key=True)
    percentage = mapped_column(Float, nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Battery(id={self.id}, percentage={self.percentage}, timestamp={self.timestamp})>"

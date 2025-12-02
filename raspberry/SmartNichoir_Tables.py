from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, Float, DateTime, create_engine

class Base(DeclarativeBase):
    pass

# --- TABLE PHOTO ---
class Photo(Base):
    __tablename__ = "photos"

    id = mapped_column(Integer, primary_key=True)
    file_name = mapped_column(String(255), nullable=False)
    file_path = mapped_column(String(255), nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)  # date + time

    def __str__(self):
        return f"{self.file_name} captured at {self.timestamp}"


# --- TABLE LOG ---
class Log(Base):
    __tablename__ = "logs"

    id = mapped_column(Integer, primary_key=True)
    message = mapped_column(String(255), nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)

    def __str__(self):
        return f"{self.timestamp}: {self.message}"


# --- TABLE BATTERY ---
class Battery(Base):
    __tablename__ = "battery"

    id = mapped_column(Integer, primary_key=True)
    percentage = mapped_column(Float, nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)

    def __str__(self):
        return f"{self.timestamp}: {self.percentage}%"


def main():
    # Connect to the SmartNichoir database
    engine = create_engine(
        "mariadb+mariadbconnector://jeremy:12345678@192.168.2.39:3306/SmartNichoir",
        echo=True
    )
    # Create all tables
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()

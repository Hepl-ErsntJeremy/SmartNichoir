from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String, DateTime

class Base(DeclarativeBase):
    pass

class Photo(Base):
    __tablename__ = "photos"

    id = mapped_column(Integer, primary_key=True)
    file_name = mapped_column(String(255), nullable=False)
    file_path = mapped_column(String(255), nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)
from sqlalchemy import Column, Integer, String
from app.database import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    seats = Column(Integer)
    location = Column(String)

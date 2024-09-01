from config.db import Base
from sqlalchemy import Column, Integer, String

#Entidad
class Movie(Base):
    #nombre de la tabla
    __tablename__ = "movies"

    #datos tabla
    id = Column(Integer, primary_key = True)
    name = Column(String)
    category = Column(String)
    year = Column(Integer)

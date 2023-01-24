from database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from flask_login import UserMixin


class Register(Base, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(80), nullable=False, unique=False)
    points = Column(Integer, unique=False, default=0)
    


class Klubs(Base):
    __tablename__ = "klubs"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=False, nullable=False)
    name_short = Column(String(20), unique=False, nullable=False)
    image = Column(String(200), unique=False, nullable=False)
    points = Column(Integer, unique=False, nullable=False)
    diff = Column(Integer, unique=False, nullable=False)
    goals_for = Column(Integer, unique=False, nullable=False)
    goals_against = Column(Integer, unique=False, nullable=False)
    matches = Column(Integer, unique=False, nullable=False)
    wins = Column(Integer, unique=False, nullable=False)
    draws = Column(Integer, unique=False, nullable=False)
    losses = Column(Integer, unique=False, nullable=False)

class Spiele(Base):
    __tablename__="spiele"

    id = Column(Integer, primary_key=True)
    spieltag = Column(Integer, unique=False, nullable=False)
    heim_team = Column(String(20), unique=False, nullable=False)
    gast_team = Column(String(20), unique=False, nullable=False)
    heim_tore = Column(Integer, unique=False, nullable=True)
    gast_tore = Column(Integer, unique=False, nullable=True)
    finished = Column(Integer, unique=False, nullable=False)
    date = Column(String(40), unique=False, nullable=False)
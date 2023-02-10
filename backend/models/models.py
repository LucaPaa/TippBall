from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin

# User-Tabelle
class Register(Base, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(80), nullable=False, unique=False)
    points = Column(Integer, unique=False, default=0)

    # Letzter getippter Spieltag
    last_tipped = Column(Integer, unique=False, nullable=False, default=0)

    comp = relationship("Tipps")

    

# Tabelle aller am Wettbewerb teilnehmenden Mannschaften
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

# Tabelle jeder einzelnen Partie, inklusive Ergebnisse
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
    started = Column(Integer, unique=False, nullable=True)
    comp = relationship("Tipps")

# Tabelle der vom Spieler abgegeben Tipps
class Tipps(Base):
    __tablename__="tipps"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=False, nullable=False)
    spiel_id = Column(Integer, ForeignKey("spiele.id"), unique=False, nullable=False)
    spieltag = Column(Integer, unique=False, nullable=False)
    heim_tore = Column(Integer, unique=False, nullable=True)
    gast_tore = Column(Integer, unique=False, nullable=True)

    # Test ob Spieler für dieses Spiel schon Punkte erhalten hat
    # noch nicht eingebunden da Punkte beim Tippen, des nächsten Spiels vergeben werden
    # in Zukunft kombinieren mit CheckUpdate
    points_awarded = Column(Integer, default = 0)

# Behälter für die letzte Aktualisierung der API
class Update(Base):
    __tablename__="update"

    id = Column(Integer, primary_key=True)
    zeit = Column(String(50), nullable=False, default="Not updated")
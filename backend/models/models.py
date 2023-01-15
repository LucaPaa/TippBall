from database.database import Base
from sqlalchemy import Column, Integer, String


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(20), unique=False, nullable=False)
    last_name = Column(String(20), unique=False, nullable=False)
    age = Column(Integer, nullable=False)
    mail = Column(String(40), nullable=False, unique=True)
    password = Column(String(20), nullable=False, unique=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"

class Klubs(Base):
    __tablename__ = "klubs"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True, nullable=False)
    name_short = Column(String(15), unique=True, nullable=False)
    image = Column(String(80), unique=True, nullable=False)
    points = Column(Integer, unique=False, nullable=False)
    diff = Column(Integer, unique=False, nullable=False)
    goals_for = Column(Integer, unique=False, nullable=False)
    goals_against = Column(Integer, unique=False, nullable=False)
    matches = Column(Integer, unique=False, nullable=False)
    wins = Column(Integer, unique=False, nullable=False)
    draws = Column(Integer, unique=False, nullable=False)
    losses = Column(Integer, unique=False, nullable=False)

    



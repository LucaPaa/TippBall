from database.database import SessionLocal
from models.models import Spiele, Klubs
from database.functions import spieltage, klubs


def init():
    with SessionLocal() as session:
        # check if spiele database is empty
        if session.query(Spiele).count() == 0:
            print("initializing spieltage...")
            # create new database
            spieltage()
            print("spieltage initialized")
        else:
            print("spieltage already initialized")
        if session.query(Klubs).count() == 0:
            print("initializing klubs...")
            # create new database
            klubs()
            print("klubs initialized")
        else:
            print("klubs already initialized")

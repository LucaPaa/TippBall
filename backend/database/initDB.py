from database.database import SessionLocal
from models.models import Spiele, Klubs
from database.functions import spieltage, klubs, aktueller, getSpieltagResults


def init():
    with SessionLocal() as session:
        # check if spiele database is empty
        if session.query(Spiele).count() == 0:
            print("initializing spieltage...")
            # create new database
            spieltage()
            print("spieltage initialized")
        else:
            #update current matchday
            getSpieltagResults(aktueller())
            print("spieltage already initialized and updated")
        
        # initializing klubs if the last playday differs from the number of matches played
        if session.query(Klubs).filter(Klubs.id ==1).value(Klubs.matches) != aktueller()-1 :
            print("initializing klubs...")
            # create new database
            klubs()
            print("klubs initialized")
        else:
            print("klubs already initialized")
            session.query(Klubs).filter(Klubs.id ==1).value(Klubs.matches)

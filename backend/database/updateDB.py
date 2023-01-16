# import schedule
# import time

# def job():
#  spieltage()
#     return


# schedule.every().minute.do(job)
# # schedule.every().day.at("22:00").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(60)  # wait one minute

from functions import aktueller
from database.database import SessionLocal
from models.models import Spiele

aktuellerSpieltag = aktueller()

with SessionLocal() as session:
    # filter by spieltag and check if finished
    games = session.query(Spiele).filter(
        Spiele.spieltag == aktuellerSpieltag).filter(Spiele.finished == 0).all()
    if len(games) == 9:
        # check result
        print("checking results...")


import json
import requests
from database.database import engine, Base, SessionLocal
from models.models import Profile, Klubs, Spiele


def spieltage():
    url = "https://api.openligadb.de/getmatchdata/bl1/2022"
    payload = {}
    headers = {
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # Turn Textfile into json for better accesability
    games = json.loads(response.text)

    for game in games:
        spieltag = game['group']
        spieltag = spieltag['groupOrderID']
        heim_team = game['team1']
        heim_team = heim_team['shortName']
        gast_team = game['team2']
        gast_team = gast_team['shortName']
        finished = game['matchIsFinished']
        date = game['matchDateTime']
        try:
            tore = game['matchResults']
            tore = tore[0]
            heim_tore = tore['pointsTeam1']
            gast_tore = tore['pointsTeam2']
        except IndexError:
            heim_tore = None
            gast_tore = None

        with SessionLocal() as session:
            g = Spiele(spieltag=spieltag, heim_team=heim_team, gast_team=gast_team,
                       heim_tore=heim_tore, gast_tore=gast_tore, finished=finished, date=date)
            session.add(g)
            session.commit()

# ToDo: check if aktueller returns current or upcoming spieltag and when it switches to the next one


def aktueller():
    url = "https://api.openligadb.de/getcurrentgroup/bl1"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    spiel_aktuell = json.loads(response.text)
    spiel_aktuell = spiel_aktuell['groupOrderID']
    return spiel_aktuell

# ToDo: consider using getlastchangedate/:leagueShortcut/:leagueSeason/:groupOrderId to check if a new update is available
# you would need some place to store your last applied update to compare against


def getSpieltagResults(spieltag):
    # format the string and append the spieltag to the url
    url = "https://api.openligadb.de/getmatchdata/bl1/2022/{}/".format(
        spieltag)

    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data={})
    spieltagresults = json.loads(response.text)

    # update the db with the results
    for game in spieltagresults:
        # ToDo: Luca will write a function that takes a game in json format and returns the models.Spiele object
        # game = jsonToSpiele(game)
        # session.add(game)
        # session.commit()
        pass


def klubs():
    # Filling the table using OpenLigaDB API
    url = "https://api.openligadb.de/getbltable/bl1/2022"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    # parse json string to python object
    table = json.loads(response.text)

    # get relevant data
    for team in table:
        name = team['teamName']
        shorty = team['shortName']
        image = team['teamIconUrl']
        points = team['points']
        goals_against = team['opponentGoals']
        goals_for = team['goals']
        matches = team['matches']
        wins = team['won']
        losses = team['lost']
        draws = team['draw']
        diff = team['goalDiff']

        with SessionLocal() as session:
            k = Klubs(name=name, name_short=shorty, image=image, points=points, diff=diff,
                      goals_against=goals_against, goals_for=goals_for, matches=matches, wins=wins,
                      losses=losses, draws=draws)
            if session.query(Klubs).count() == 18:
                session.flush(k)
                session.commit()
            else:
                session.add(k)
                session.commit()


def checkNewResultsSpieltag():
    with SessionLocal() as session:
        spieltag = aktueller()
        # check if spieltag in db is finished
        if session.query(Spiele).filter(Spiele.spieltag == spieltag).filter(Spiele.finished == 1).count() == 0:
            print("Spieltag finished, skipping update")
            return
        else:
            print("Spieltag not finished, updating...")
            getSpieltagResults(spieltag)
            klubs()


def checkSpieltageThread():
    import schedule
    import time

    # ToDo: adjust schedule???
    #  function is now way faster so anything above a minute shoudl suffice
    #  could also consider making this configurable through env variables?
    # e.g. if TIPPBALL_UPDATE_INTERVAL == "minute"/"hour"/"day" etc
    schedule.every().minute.do(checkNewResultsSpieltag)
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
    # schedule.every().day.at("22:00").do(job)

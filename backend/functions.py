
import json
import requests
from database.database import engine, Base, SessionLocal
from models.models import Profile, Klubs, Spiele

# import the database session
Base.metadata.create_all(engine)

def spieltage():
    url = "https://api.openligadb.de/getmatchdata/bl1/2022"
    payload={}
    headers = {
    'Accept': 'text/plain'
    }
    response_2 = requests.request("GET", url, headers=headers, data=payload)
    #Turn Textfile into json for better accesability
    games = json.loads(response_2.text)

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
            if Spiele.id != 9*34 :
                session.add(g)
                session.commit()
            else:
                session.flush(g)
                session.commit()

def aktueller():
    url = "https://api.openligadb.de/getcurrentgroup/bl1"

    payload={}
    headers = {
    'Accept': 'text/plain'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    spiel_aktuell = json.loads(response.text)
    spiel_aktuell = spiel_aktuell['groupOrderID']
    return spiel_aktuell

def filltable():
    #Creating the table using OpenLigaDB API

    url = "https://api.openligadb.de/getbltable/bl1/2022"

    payload={}
    headers = {
    'Accept': 'text/plain'
    }
    response_1 = requests.request("GET", url, headers=headers, data=payload)

    #Turn Textfile into json for better accesability
    table = json.loads(response_1.text)

    #get relevant data
    for team in table:
        name = team['teamName']
        shorty = team['shortName']
        image = team['teamIconUrl']
        points = team['points']
        goals_against = team['opponentGoals']
        goals_for = team['goals']
        matches = team['matches']
        wins = team['won']
        losses= team['lost']
        draws = team['draw']
        diff = team['goalDiff']

        with SessionLocal() as session:
            k = Klubs(name=name, name_short=shorty, image=image, points=points, diff=diff,
                        goals_against=goals_against, goals_for=goals_for, matches=matches, wins=wins,
                        losses=losses, draws=draws)
            if session.query(Klubs).count()==18:
                session.flush(k)
                session.commit()
            else:
                session.add(k)
                session.commit()
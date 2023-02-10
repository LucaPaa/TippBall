
import json
import requests
from database.database import engine, Base, SessionLocal
from models.models import Klubs, Spiele, Update, Tipps, Register

# generates game schedule
def spieltage():
    url = "https://api.openligadb.de/getmatchdata/bl1/2022"
    payload = {}
    headers = {
        'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    games = json.loads(response.text)

    #recieve relevant data to generate all games of the 2022/23 bundesliga-season
    for game in games:
        spieltag = game['group']
        spieltag = spieltag['groupOrderID']
        heim_team = game['team1']
        heim_team = heim_team['shortName']
        gast_team = game['team2']
        gast_team = gast_team['shortName']
        finished = game['matchIsFinished']
        date = game['matchDateTime']

    # throws an exception when goal colums are empty if database is initialized when games already have been played
    # not finished games will recieve "None" goals
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
# Edit: aktueller switches halfway between matchdays

# returns the current matchday --> changes between weeks, e.g. on a regular schedule on wednesday (not the girl from the adams family tho)
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
# you would need some place to store your last applied update to compare against --> Done

def checkUpdate():
    # format the string and append the  current matchday to the url
    url = "https://api.openligadb.de/getlastchangedate/bl1/2022/{}/".format(aktueller())

    payload={}
    headers = {
        'Accept': 'text/plain'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    changedate = json.loads(response.text)
    with SessionLocal() as session:
        date = session.query(Update).get(1)
        #check if a newer information are availabe and update database object if neccesary
        if changedate.startswith("2023") and changedate != date.zeit:
            date.zeit = changedate
            session.commit()
            print("time actualized")
        else:
            print("time is up to date")

# if database is initialized this returns the last date of change in data
def getChangeDate(spieltag):
    # format the string and append the match to the url
    url = "https://api.openligadb.de/getlastchangedate/bl1/2022/{}/".format(spieltag)

    payload={}
    headers = {
        'Accept': 'text/plain'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    changedate = json.loads(response.text)
    with SessionLocal() as session:
        u = Update(zeit = changedate)
        session.add(u)
        session.commit()
    
# returns the result for a chosen macth day and updates the game schedule
def getSpieltagResults(spieltag):
    # format the string and append the spieltag to the url
    url = "https://api.openligadb.de/getmatchdata/bl1/2022/{}/".format(
        spieltag)

    headers = {
        'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data={})
    spieltagresults = json.loads(response.text)
    i = 1

    # update the db with the results
    # chose a kinda sloppy/sussy fix has to be optimized in the future
    for game in spieltagresults:
        finished = game['matchIsFinished']
        spieltag = game['group']
        spieltag = spieltag['groupOrderID']
        started = 1

        try:
            tore = game['matchResults']
            tore = tore[0]
            heim_tore = tore['pointsTeam1']
            gast_tore = tore['pointsTeam2']

        # some matches are played later on the same matchday so we throw an excpetion for them once again
        except IndexError:
            heim_tore = None
            gast_tore = None
            started = 0    
        
        with SessionLocal() as session:
            #games are easily countable --> formula to get the games of the current match day
            # works tested 25.01.2023 Mainz-BVB
            spiel = session.query(Spiele).get((aktueller()-1)*9+i)
            spiel.finished = finished
            spiel.heim_tore = heim_tore
            spiel.gast_tore = gast_tore
            # started = null --> match is long over
            # started = 0 --> match is in current matchday and hasnt  started
            # started = 1 --> match is in current matchday and has started
            spiel.started = started
            session.commit()
            i = i + 1

    return spieltag

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


        #keeping table updated and in correct order with delete --> restore
        #prefer updating, need to figure out how to order in html/css
        with SessionLocal() as session:
            k = Klubs(name=name, name_short=shorty, image=image, points=points, diff=diff,
                      goals_against=goals_against, goals_for=goals_for, matches=matches, wins=wins,
                      losses=losses, draws=draws)
            if session.query(Klubs).count() == 18:
                session.query(Klubs).delete()
                session.add(k)
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

def awardPoints(user):
    with SessionLocal() as session:
        spieltag = aktueller()-1
        spiele = session.query(Spiele).filter(Spiele.spieltag==spieltag)
        tipps = session.query(Tipps).filter(Tipps.spieltag==spieltag).filter(Tipps.user_id==user)

        tore_heim = []
        tore_gast = []
        tipp_heim = []
        tipp_gast = []

        for spiel in spiele:
          tore_heim.append(spiel.heim_tore)
          tore_gast.append(spiel.gast_tore)
        for tipp in tipps:
          tipp_heim.append(tipp.heim_tore)
          tipp_gast.append(tipp.gast_tore)

        points = 0
        #Berechnung entfällt, wenn der vorherige Spieltag nicht getippt wurde
        if len(tore_heim) == len(tipp_heim):
            for i in range(9):
                diff_spiel = tore_heim[i] - tore_gast[i]
                diff_tipp = tipp_heim[i] - tipp_gast[i]
                # 0 --> Unentschieden
                # positiver Wert --> Sieg Heim
                # negativer Wert --> Sieg Gast

                #jeweils genaues ergebnis, differenz sieg heim/gast, tendenz sieg heim/gast, sonst 0 punkte
                if tore_heim[i] == tipp_heim[i] and tore_gast[i] == tipp_gast[i]:
                    points = points + 3
                elif diff_spiel > 0 and diff_tipp > 0 and diff_tipp == diff_spiel:
                    points = points + 2
                elif diff_spiel < 0 and diff_tipp < 0 and diff_tipp == diff_spiel:
                    points = points + 2
                elif diff_spiel > 0 and diff_tipp > 0 and diff_tipp != diff_spiel:
                    points = points + 1
                elif diff_spiel < 0 and diff_tipp < 0 and diff_tipp != diff_spiel:
                    points = points + 1
                else:
                    points = points + 0
            reward = session.query(Register).get(user)
            print(reward.username)
            reward.points = reward.points + points
            session.commit()
                

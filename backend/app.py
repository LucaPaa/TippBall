import json
import os
from flask import Flask, render_template, redirect, request

from models.models import Profile, Klubs, Spiele
from database.database import engine, Base, SessionLocal
import requests

app = Flask(__name__)

app.app_context().push()

# import the database session
Base.metadata.create_all(engine)


@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')

@app.route('/add', methods=["POST"])
def profile():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")
    mail = request.form.get("mail")
    password = request.form.get("password")

    if first_name != '' and last_name != '' and age is not None and mail != '' and password != '':
        with SessionLocal() as session:
            p = Profile(first_name=first_name, last_name=last_name,
                        age=age, mail=mail, password=password)
            session.add(p)
            session.commit()
        return redirect('/profile')
    else:
        return redirect('/profile')

# currently nur amogus


@app.route('/')
def index():
    return render_template('bundesliga.html')


@app.route('/profile')
def profil():
    with SessionLocal() as session:
        profiles = session.query(Profile).all()
    return render_template('profile.html', profiles=profiles)

# currently nur amogus


@app.route('/tipps')
def tipps():
    return render_template('tipps.html')

# currently nur amogus


@app.route('/gruppen')
def gruppen():
    return render_template('gruppen.html')


@app.route('/delete/<int:id>')
def erase(id: str):
    with SessionLocal() as session:
        data = session.query(Profile).filter_by(id=id).first()
        session.delete(data)
        session.commit()
    return redirect('/profile')

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

@app.route('/tabelle')
def tabelle():
    with SessionLocal() as session:
        klubs = session.query(Klubs).all()
    return render_template('tabelle.html', klubs=klubs)


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

if __name__ == '__main__':
   app.run(debug=True)


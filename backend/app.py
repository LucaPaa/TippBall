import json
import os
from flask import Flask, render_template, redirect, request
from database.functions import spieltage, aktueller, checkSpieltageThread
from models.models import Profile, Klubs, Spiele
from database.database import engine, Base, SessionLocal
from database.initDB import init
import requests

app = Flask(__name__)

app.app_context().push()

# import the database session
Base.metadata.create_all(engine)

saison = 2022


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


@app.route('/partien')
def partien():
    with SessionLocal() as session:
        spiele = session.query(Spiele).filter(Spiele.spieltag == aktueller()-1)
        print(spiele)
    return render_template('partien.html', spiele=spiele)


@app.route('/delete/<int:id>')
def erase(id: str):
    with SessionLocal() as session:
        data = session.query(Profile).filter_by(id=id).first()
        session.delete(data)
        session.commit()
    return redirect('/profile')


@app.route('/tabelle')
def tabelle():
    with SessionLocal() as session:
        klubs = session.query(Klubs).all()
    return render_template('tabelle.html', klubs=klubs)


if __name__ == '__main__':
    # check if env vraibles are set
    # TODO: automatically set the correct one (check time.Now for august)


    #if os.environ.get('TIPPBALL_SAISON') is None:
    #    print("TIPPBALL_SAISON is not set. Using 2022")
    #else:
    #    saison = os.environ.get('TIPPBALL_SAISON')

    # init the database

    init()

    # start a background task to update the database (spieltage)

    #import threading
    #t = threading.Thread(target=checkSpieltageThread)
    #t.start()

    # start the webserver

    app.run(debug=True)

import os
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('bundesliga.html')

@app.route('/tipps')
def tipps():
    return render_template('tipps.html')

@app.route('/gruppen')
def gruppen():
    return render_template('gruppen.html')

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Benutzername', [validators.Length(min=6, max=12)])
    email = StringField('Email', [validators.Length(min=6, max= 50)])
    password = PasswordField('Passwort',[
        validators.DataRequired(),
        validators.EqualTo('confirm ', message= 'Die Passwörter stimmen nicht überein')
    ])
    confirm = PasswordField('Bestätige Passwort')

@app.route('/registrierung', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

            return render_template('register.html', form=form)  
    return render_template('register.html', form=form)  

if __name__ == '__main__':
    app.run(debug = True)
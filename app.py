import os
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, validators
from flask_migrate import Migrate
# import db

app = Flask(__name__)

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()
 
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)
#Joni pls explain

# Models
# Kann ich dies auch in einer anderen .py ansiedeln und wie UND wie update ich die db gescheit ohne immer
# alles aus dem migrations- und instance ordner zu löschieren
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    mail = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False, unique=False)
 
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"
 

@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')

# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
     
    # In this function we will input data from the
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")
    mail = request.form.get("mail")
    password = request.form.get("password")
 
    # create an object of the Profile class of models
    # and store data as a row in our datatable
    if first_name != '' and last_name != '' and age is not None and mail != '' and password != '':
        p = Profile(first_name=first_name, last_name=last_name, age=age, mail=mail, password=password)
        db.session.add(p)
        db.session.commit()
        return redirect('/profile')
    else:
        return redirect('/profile')

@app.route('/')
def index():
    return render_template('bundesliga.html')

@app.route('/profile')
def profil():
    profiles = Profile.query.all()
    return render_template('profile.html', profiles=profiles)

@app.route('/tipps')
def tipps():
    return render_template('tipps.html')

@app.route('/gruppen')
def gruppen():
    return render_template('gruppen.html')

# Remnant from a forgotten age
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

@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and
    # redirects to home page
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/profile')

if __name__ == '__main__':
    app.run(debug = True)
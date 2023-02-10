from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from database.functions import aktueller
from models.models import Register
from database.database import SessionLocal

# Formular zum Tippen des Spieltags
class TippForm(FlaskForm):
    h0 = IntegerField(validators=[InputRequired()])
    h1 = IntegerField(validators=[InputRequired()])
    h2 = IntegerField(validators=[InputRequired()])
    h3 = IntegerField(validators=[InputRequired()])
    h4 = IntegerField(validators=[InputRequired()])
    h5 = IntegerField(validators=[InputRequired()])
    h6 = IntegerField(validators=[InputRequired()])
    h7 = IntegerField(validators=[InputRequired()])
    h8 = IntegerField(validators=[InputRequired()])
    g0 = IntegerField(validators=[InputRequired()])
    g1 = IntegerField(validators=[InputRequired()])
    g2 = IntegerField(validators=[InputRequired()])
    g3 = IntegerField(validators=[InputRequired()])
    g4 = IntegerField(validators=[InputRequired()])
    g5 = IntegerField(validators=[InputRequired()])
    g6 = IntegerField(validators=[InputRequired()])
    g7 = IntegerField(validators=[InputRequired()])
    g8 = IntegerField(validators=[InputRequired()])

    submit = SubmitField('Tipps absenden')

# Formular zum Auswählen des Spieltags
class SelectForm(FlaskForm):
    spieltage = SelectField('spieltag', choices=[], default=aktueller())

# Formular zum Registrieren auf der Website
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Benutzername"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Passwort"})

    submit = SubmitField('Registrieren')

    def validate_username(self, username):
        with SessionLocal() as session:
            existing_user_username = session.query(Register).filter_by(
                username=username.data).first()
            if existing_user_username:
                raise ValidationError('Der Benutzername existiert bereits.')

# Login-Formular
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Benutzername"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Passwort"})

    submit = SubmitField('Login')
from flask import Flask, render_template, redirect, request
from database.functions import spieltage, aktueller, checkSpieltageThread, getSpieltagResults
from models.models import Klubs, Spiele, Register
from database.database import engine, Base, SessionLocal
from database.initDB import init
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)

app.app_context().push()
app.secret_key = "thisissecret"

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as session:
        return session.query(Register).get(int(user_id))

# import the database session
Base.metadata.create_all(engine)

saison = 2022

class SelectForm(FlaskForm):
    spieltage = SelectField('spieltag', choices=[])

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

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Benutzername"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Passwort"})

    submit = SubmitField('Login')

#Start of routing
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('bundesliga.html')
    else: 
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        with SessionLocal() as session: 
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = Register(username=form.username.data, password=hashed_password)
            session.add(new_user)
            session.commit()
            return redirect('/login')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with SessionLocal() as session:
            user = session.query(Register).filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect('/start')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')
            

@app.route('/start')
@login_required
def start():
    return render_template('bundesliga.html')


# currently nur amogus
@app.route('/tipps')
def tipps():
    return render_template('tipps.html')

@app.route('/score')
def score():
    return render_template('score.html')



@app.route('/partien', methods= ['GET', 'POST'])
def partien():
    form = SelectForm()
    with SessionLocal() as session:
        # we do a little bit of hard-coding --> tb optimize
        form.spieltage.choices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]
        spiele = session.query(Spiele).filter(Spiele.spieltag == aktueller())
    if request.method == 'POST':
        path = '/partien/{}'.format(form.spieltage.data)
        return redirect(path)
    tag = aktueller()
    return render_template('partien.html', spiele=spiele, form=form, tag=tag)

@app.route('/partien/<id>', methods=['GET', 'POST'])
def partien_choice(id):
    form = SelectForm()
    tag = id
    with SessionLocal() as session:
        # we do a little bit of hard-coding --> tb optimize
        form.spieltage.choices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]
        spiele = session.query(Spiele).filter(Spiele.spieltag == id)
    
    if request.method == 'POST':
        path = '/partien/{}'.format(form.spieltage.data)
        return redirect(path)
    return render_template('partien.html', spiele=spiele, form=form, tag=tag)    

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
    

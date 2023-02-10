from flask import Flask, render_template, redirect, request
from database.functions import aktueller, checkUpdate, awardPoints
from models.models import Klubs, Spiele, Register, Tipps
from database.database import engine, Base, SessionLocal
from database.initDB import init
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from models.forms import SelectForm, TippForm, RegisterForm, LoginForm

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

#möglicherweise dynamisch gestalten, um Spielen über einen längeren Zeitraum zu ermöglichen
saison = 2022

#Startpunkt des Routings
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return render_template('bundesliga.html', user = current_user)
    else: 
        return render_template('index.html')

#Registrierungsplattform
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

#Loginplattform
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
            
# Landing-Page
@app.route('/start')
@login_required
def start():
    return render_template('bundesliga.html', user = current_user)


#optimierung mit for-loop wünschenswert jedoch erschließt sich mir nicht warum jinja das blockiert
#spiele die als nicht als spiel.started = 1 sind tippbar, da momentan nur der aktuellste spieltag angezeigt wird verschinden spiele die bereits gestartet sind
@app.route('/tipps', methods= ['GET', 'POST'])
@login_required
def tipps():
    form = TippForm()
    with SessionLocal() as session:
        #zum Testen am vorherigen spieltag die funktionsausfrufe von aktueller um 1 reduzieren und im tipps.html if bedingung auf z.B. start == 0 anpassen
        #die spiele verschwinden aus dem form
        #bei verpassten spielen werden die IntegerFields deaktiviert und ihnen wird der Wert -1 zugewiesen
        #so kann der Validator noch berücksichtigt werden 
        spiele = session.query(Spiele).filter(Spiele.spieltag == aktueller())
        tipptest = current_user.last_tipped
        #redundante if-Abfrage unbedingt in Zukunft beheben, für Testzwecke vorerst behalten
        if tipptest != aktueller():
            if form.validate_on_submit():
                if tipptest != aktueller():
                    tipps = [[] for spiel in spiele]
                    tipps[0] = [form.h0.data, form.g0.data]
                    tipps[1] = [form.h1.data, form.g1.data]
                    tipps[2] = [form.h2.data, form.g2.data]
                    tipps[3] = [form.h3.data, form.g3.data]
                    tipps[4] = [form.h4.data, form.g4.data]
                    tipps[5] = [form.h5.data, form.g5.data]
                    tipps[6] = [form.h6.data, form.g6.data]
                    tipps[7] = [form.h7.data, form.g7.data]
                    tipps[8] = [form.h8.data, form.g8.data]
                    i = 0
                    for spiel in spiele:
                        user = current_user.id
                        spieltag = spiel.spieltag
                        spiel_id = spiel.id
                        heim_tore = tipps[i][0]
                        gast_tore = tipps[i][1]
                        t = Tipps(user_id = user, spiel_id = spiel_id, spieltag=spieltag, heim_tore=heim_tore, gast_tore=gast_tore)
                        session.add(t)
                        print(tipps[i])
                        i = i+1
                    done = session.query(Register).get(current_user.id)
                    done.last_tipped = aktueller()
                    session.commit()
                    #wegen dem bewerten durch tippen des nächsten Tages kann ja nicht der 0. Spieltag belohnt werden
                    #gleiches problem mit dem letzten Spieltag das muss in Zukunft über checkUpdate geregelt werden
                    if aktueller() > 1:
                        awardPoints(current_user.id)
                    return redirect('/start')    
                    # html page mit den letzten tipps
            return render_template('tipps.html', user=current_user, form=form, spiele=spiele)
        else:
            return redirect('/review')

#wenn die Spiele getippt wurden werden hier die tipps angezeigt       
@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    with SessionLocal() as session:
        spiele = session.query(Spiele).filter(Spiele.spieltag == aktueller())
        tipps = session.query(Tipps).filter(Tipps.spieltag == aktueller()).filter(Tipps.user_id == current_user.id)
    return render_template('review.html', tipps=tipps, spiele=spiele)

# Beinhaltet eine Liste aller Spieler und deren Punkte       
@app.route('/score')
@login_required
def score():
    with SessionLocal() as session:
        users = session.query(Register).all()
        return render_template('score.html', user = current_user, users= users)


# Beinhaltet zunächst die Partien des aktuellen Spieltags
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

# Beinhaltet sämtlich Partien jeden Spieltags, zugänglich über ein Dropdown-Menü
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
    return render_template('partien.html', spiele=spiele, form=form, tag=tag, user = current_user)    

# Ausgabe der aktuellen Bundesliga-Tabelle
@app.route('/tabelle')
def tabelle():
    with SessionLocal() as session:
        klubs = session.query(Klubs).all()
    return render_template('tabelle.html', klubs=klubs)


if __name__ == '__main__':
    # initiiere die Datenbank
    init()
    # an dieser Stelle vielleicht später noch Multi-Threading hinzufügen, um Datenbank regelmäßig zu "füttern"
    
    # überprüfen ob neuere Inhalte der API vorliegen
    checkUpdate()

    # Starten der Anwendung setz "debug=True" um im Debugger-Modus zu starten
    app.run(debug=True)
    

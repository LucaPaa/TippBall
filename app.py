import os
from flask import Flask
import db

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'todos.sqlite')
)
app.cli.add_command(db.init)
app.teardown_appcontext(db.close)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hallo Bundesliga!'

@app.route('/insert/sample')
def insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'
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

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/wow')
def wow():
    return 'Wow, this is my second working URL!'

@app.route('/insert/sample')
def insert_sample():
    db.insert_sample()
    return 'Database flushed and populated with some sample data.'
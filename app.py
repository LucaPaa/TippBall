import os
from flask import Flask, render_template
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


if __name__ == '__main__':
    app.run(debug = True)
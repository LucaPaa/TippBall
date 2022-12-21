import os
from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bundesliga.html')

if __name__ == '__main__':
    app.run(debug = True)
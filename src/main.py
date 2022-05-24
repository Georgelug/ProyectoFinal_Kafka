# server donde van a estar los brokers
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms.fields import SubmitField

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'awa de uwu'

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
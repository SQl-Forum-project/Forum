from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SECRET_KEY'] ='secret'
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'ye ye'
class Forumdg(db.Model):
    __tablename__ = 'forumdg2'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"
@app.route('/')
def home():
    return render_template('index.html')

temp=0
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        try:
            usn = request.form['usn']
            psd = request.form['psd']
            em = request.form['em']
            just1 = Forumdg(username=usn, password=psd, email=em)
            db.session.add(just1)
            db.session.commit()
            flash('Sign In Succesfully')
            return render_template('index.html',flag=1)
        except:
            flash('Username and Password already exist')
            return render_template('index.html',flag=1)

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global eml
        global usnl
        usnl = request.form['usnl']
        psdl = request.form['psdl']
        eml = request.form['eml']
        try:
            cheking = Forumdg.query.filter_by(
                username=usnl, password=psdl, email=eml).first()
            if not cheking:
                flash('Username and Password Are Incorrect')
                return render_template('index.html',flag=2)
            else:
                # flash('login In Succesfully')
                global temp
                temp = 1
                return "HH"
        except:
            flash('Username and Password Are Incorrect')
            return render_template('index.html')
    return render_template('index.html')
if(__name__)=='__main__':
    app.run(debug=True)

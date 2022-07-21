from flask import Blueprint, flash, render_template, request, session
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from model.User import User
login = Blueprint(name="login", import_name=__name__)


@login.route('/', methods=['GET', 'POST'])
def logIn():
    if request.method == 'POST':
        global eml
        global usnl
        usnl = request.form['usnl']
        psdl = request.form['psdl']
        eml = request.form['eml']
        hashed_Value = generate_password_hash(psdl)
        print(hashed_Value)
        try:
            cheking = User.query.filter_by(
                username=usnl, email=eml, flags=True).first()
            print(check_password_hash(cheking.password, psdl))
            if not cheking:
                flash('Username and Email Are Incorrect')
                return render_template('index.html', flag=2)
            elif cheking and check_password_hash(cheking.password, psdl):
                login_user(cheking)
                session['visits'] = cheking.id
                print("LOl", cheking.id)
                user = User.query.filter_by(id=session.get('visits')).first()
                return render_template('forums.html', user=user)
            else:
                flash('Password Is Incorrect')
                return render_template('index.html', flag=2)
        except Exception as e:
            print(e)
            flash('Username and Password Are Incorrect')
            return render_template('index.html', flag=2)
    return render_template('index.html')

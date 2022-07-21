import os
from flask import Blueprint, flash, render_template, request
from model.User import User
from . import s
from helper.mail import send_mail
from werkzeug.security import generate_password_hash, check_password_hash
signin = Blueprint(name="signin", import_name=__name__)


@signin.route('/', methods=['POST', 'GET'])
def signIn():
    global usn
    global psd
    global em
    if request.method == 'POST':
        try:
            usn = request.form['usn']
            psd = request.form['psd']
            em = request.form['em']
            check_if_exsisit_email = User.query.filter_by(email=em).first()
            check_if_exsisit_username = User.query.filter_by(
                username=usn).first()
            hashed_Value = generate_password_hash(psd)
            check_if_exsisit_password = User.query.filter_by(
                password=hashed_Value).first()
            if not check_if_exsisit_email and not check_if_exsisit_username and not check_if_exsisit_password:
                hashed_Value = generate_password_hash(psd)
                print(hashed_Value)
                print(check_password_hash(hashed_Value, psd))
                token = s.dumps(
                    {"Email": em, "Password": hashed_Value, "Username": usn}, salt='email-confirm')
                mail = send_mail(em, 'Auth Token', token)
                if mail:
                    flash('Check Mail For Authentication')
                else:
                    flash('Something Went Wrong')
                return render_template('index.html', flag=1)
            else:
                flash('User Already Exist')
                return render_template('index.html', flag=1)
        except Exception as e:
            print(e)
            flash('Use Diffrent Username and Password')
            return render_template('index.html', flag=1)

    return render_template('index.html')

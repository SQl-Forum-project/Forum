from werkzeug.security import generate_password_hash
from model.User import User
from model import db
from . import s
from flask import Blueprint, redirect, render_template, request
from itsdangerous import BadSignature, SignatureExpired
reset_password = Blueprint(name="reset_password", import_name=__name__)


@reset_password.route('/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        data = s.loads(token, salt='email-reset', max_age=60)
        if request.method == 'GET':
            user_profile = User.query.filter_by(email=data["Email"]).first()
            return render_template('Search_bar.html', token=token, user=user_profile)
        if request.method == 'POST':
            reset_password = request.form["reset_password"]
            print(reset_password)
            hashed_Value = generate_password_hash(reset_password)
            print(hashed_Value)
            print(data["Email"])
            user_profile = User.query.filter_by(email=data["Email"]).first()
            user_profile.password = hashed_Value
            db.session.add(user_profile)
            db.session.commit()
            return redirect('/')
    except SignatureExpired:
        return "The Token Is Expired"
    except BadSignature:
        return "The token is invalid"
    return "This email worked"

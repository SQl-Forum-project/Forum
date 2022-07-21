from model.User import User
from model import db
from . import s
from flask import Blueprint
from itsdangerous import BadSignature, SignatureExpired
confirm_email = Blueprint(name="confirm_email", import_name=__name__)


@confirm_email.route('/<token>')
def confirm_emails(token):
    try:
        data = s.loads(token, salt='email-confirm', max_age=60)
        conf = User(username=data["Username"], email=data["Email"],
                    password=data["Password"], flags=True)
        db.session.add(conf)
        db.session.commit()
    except SignatureExpired:
        return "The Token Is Expired"
    except BadSignature:
        return "The token is invalid"
    return "This email worked"

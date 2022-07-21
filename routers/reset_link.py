from . import s
from model.User import User
from flask import Blueprint, request
from helper.mail import send_mail
reset_link = Blueprint(name="reset_link", import_name=__name__)


@reset_link.route('/', methods=['GET', 'POST'])
def reset_links():
    if request.method == 'POST':
        reset_email = request.form['emailforget']
        cheking = User.query.filter_by(email=reset_email, flags=True).first()
        if not cheking:
            return "User Doesn't Exist"
        reset_token = s.dumps({"Email": reset_email}, salt='email-reset')
        print(reset_token)
        mail = send_mail(reset_email, 'Reset Password', reset_token)
        if mail:
            return "Check Mail For Reset Password"
        else:
            return "Something Went Wrong"

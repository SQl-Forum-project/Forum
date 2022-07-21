from model.User import User
from flask import Blueprint, render_template, request
userprofile = Blueprint(name="userprofile", import_name=__name__)


@userprofile.route('/<string:username>', methods=['GET', 'POST'])
def userprofile(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if not user:
            return "Not Fund"
        return render_template('user_profile.html', user=user)
    user = User.query.filter_by(username=username).first()
    if not user:
        return "Not Fund"
    return render_template('user_profile.html', user=user)

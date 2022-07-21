from flask import Blueprint, flash, render_template, request, session
from flask_login import login_required
from model import db
from model.Forum import Forum
from model.User import User
askque = Blueprint(name="askque", import_name=__name__)


@askque.route('/askque', methods=['GET', 'POST'])
@login_required
def askques():
    if request.method == 'POST':
        topic = request.form['tpc']
        Discription = request.form['tpcdisc']
        askingquestion = Forum(user_id=session.get(
            'visits'), title=topic, discription=Discription)
        db.session.add(askingquestion)
        db.session.commit()
        user_profile = User.query.filter_by(id=session.get('visits')).first()
    flash('Question Ask')
    return render_template('forums.html', flag=1, user=user_profile)

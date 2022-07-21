from flask import Blueprint, redirect, request, session
from flask_login import login_required
from model import db
from model.Forum import Forum

replay = Blueprint(name="replay", import_name=__name__)


@replay.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def replays(id):
    if request.method == 'POST':
        comment = request.form["ncom"]
        replay_msg = Forum(user_id=session.get('visits'),
                           flag=id, discription=comment)
        db.session.add(replay_msg)
        db.session.commit()
        print(comment)
        return redirect(f'/forum/{id}')

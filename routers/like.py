from model.Like import Like
from model import db
from flask import Blueprint, request, session
like = Blueprint(name="like", import_name=__name__)


@like.route('/like', methods=['GET', 'POST'])
def like():
    if request.method == 'POST':
        res = int(request.form.get('data'))
        lk = Like(userid=session.get('visits'), forumid=res)
        db.session.add(lk)
        db.session.commit()
    return "render"

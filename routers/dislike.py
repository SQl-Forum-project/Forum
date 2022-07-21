from model.Like import Like
from model import db
from operator import and_
from flask import Blueprint, request, session
dislike = Blueprint(name="dislike", import_name=__name__)


@dislike.route('/', methods=['GET', 'POST'])
def dislikes():
    if request.method == 'POST':
        res = int(request.form.get('data'))
        db.session.query(Like).filter(and_(Like.forumid == int(
            res), Like.userid == session.get('visits'))).delete()
        db.session.commit()
    return "render"

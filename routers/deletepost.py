from model import db
from flask import Blueprint, request
deletepost = Blueprint(name="deletepost", import_name=__name__)


@deletepost.route('/', methods=['GET', 'POST'])
def deletepost():
    if request.method == 'POST':
        re = request.form.get('data')
        res = int(re)
        print(res)
        db.session.execute(f'DELETE FROM forum_like WHERE forumid={res}')
        db.session.commit()
        db.session.execute(f'DELETE FROM forum_reply WHERE flag={res}')
        db.session.commit()
        db.session.execute(f'DELETE FROM forum WHERE id={res}')
        db.session.commit()

        print(res)
    return "render"

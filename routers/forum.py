from model.User import User
from model.Forum import Forum
from model.Reply import Reply
from model import db
from flask import Blueprint, render_template, session
from flask_login import login_required
from operator import and_

forum = Blueprint(name="forum", import_name=__name__)


@forum.route('/')
@login_required
def forum():
    user = list(db.session.query(User.Image_Str, User.username, User.id)
                .join(Forum, User.id == Forum.user_id)
                .all())
    temp_like = db.session.execute(
        'SELECT COUNT (forum_like.forumid),forum.id , forum.title,forum.discription FROM forum_like RIGHT JOIN forum ON forum_like.forumid = forum.id GROUP BY forum.id ORDER BY forum.id').fetchall()
    lenghts = len(temp_like)
    te = session.get('visits')
    flgs_db = db.session.execute(
        f'SELECT forum_like.forumid FROM forum_like RIGHT JOIN forum ON forum_like.userid = {te} AND forum.id = forum_like.forumid').fetchall()
    return render_template('test.html', ques=temp_like, user=user, total_len=lenghts, like=flgs_db, curruser=session.get('visits'))


@forum.route('/<int:id>',methods=['GET','POST'])
@login_required
def forum_id(id):
    forum_gg = Forum.query.filter_by(id=id).first()
    user =list(db.session.query(User.Image_Str,User.username)
                                .join(Forum, User.id == forum_gg.user_id)
                                .first())
    users =list(db.session.query(User.Image_Str,User.username,Reply.discription).join(Reply,and_(Reply.flag==id , User.id == Reply.user_id)).all())
    print(users)
    return render_template('bbg.html',ques=forum_gg,user=user,users=users,lenghtsq=len(users))
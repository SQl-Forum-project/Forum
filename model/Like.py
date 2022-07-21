from . import db
class Like(db.Model):
    __tablename__ = 'forum_like'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    forumid = db.Column(db.Integer, db.ForeignKey('forum.id'))
    def __repr__(self) -> str:
        return f"{self.forumid} - {self.userid}"
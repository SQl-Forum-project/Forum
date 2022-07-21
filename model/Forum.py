from datetime import datetime
from . import db
class Forum(db.Model):
    __tablename__ = "forum"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    title = db.Column(db.String)
    discription = db.Column(db.String)
    time = db.Column(db.Date,default=datetime.now)
    def __repr__(self) -> str:
        return f"{self.id} - {self.user_id}"
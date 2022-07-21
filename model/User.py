from . import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    flags = db.Column(db.Boolean, default=False)
    usernamefull = db.Column(db.String, default="NOT_SET")
    Location = db.Column(db.String, default="NOT_SET")
    Bio = db.Column(db.String, default="NOT_SET")
    Image_Str = db.Column(db.String, default="1")
    Designation = db.Column(db.String, default="NOT_SET")
    phone = db.Column(db.String, default="NOT_SET")
    Instagram = db.Column(db.String, default="NOT_SET")
    Facebook = db.Column(db.String, default="NOT_SET")
    Twitter = db.Column(db.String, default="NOT_SET")
    Github = db.Column(db.String, default="NOT_SET")
    Linkdin = db.Column(db.String, default="NOT_SET")
    website = db.Column(db.String, default="NOT_SET")
    DOB = db.Column(db.Date, default='08-01-2003')

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

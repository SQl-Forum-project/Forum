from . import login_manager
from model.User import User
from flask_login import AnonymousUserMixin
login_manager.login_view = 'login.logins'
class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
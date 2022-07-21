import os
from dotenv import load_dotenv
from model import db
from middleware import login_manager
from routers import index,signin,login,like,reset_password,userprofile,askque,logout,confirm_email,reset_link,dislike,editprofile,deletepost,forum,replay
def create_app(app):
    load_dotenv('.env')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    uri =  os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'ye ye'
    app.config['JSON_AS_ASCII'] = False
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(index.index,url_prefix='/')
    app.register_blueprint(login.login,url_prefix='/login')
    app.register_blueprint(signin.signin,url_prefix='/signin')
    app.register_blueprint(like.like,url_prefix='/like')
    app.register_blueprint(reset_password.reset_password,url_prefix='/reset_password')
    app.register_blueprint(userprofile.userprofile,url_prefix='/userprofile')
    app.register_blueprint(logout.logout,url_prefix='/logout')
    app.register_blueprint(askque.askque,url_prefix='/askque')
    app.register_blueprint(confirm_email.confirm_email,url_prefix='/confirm_email')
    app.register_blueprint(reset_link.reset_link,url_prefix='/reset_link')
    app.register_blueprint(dislike.dislike,url_prefix='/dislike')
    app.register_blueprint(editprofile.editprofile,url_prefix='/editprofile')
    app.register_blueprint(deletepost.deletepost,url_prefix='/deletepost')
    app.register_blueprint(forum.forum,url_prefix='/forum')
    app.register_blueprint(replay.replay,url_prefix='/replay')
    return app
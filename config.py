import os
from dotenv import load_dotenv
from model import db
from middleware import login_manager
from routers import index,signin,login,like,reset_password,userprofile,askque,logout,confirm_email,reset_link,dislike,editprofile,deletepost,forum,replay
def create_app(app):
    load_dotenv('.env')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'ye ye'
    app.config['JSON_AS_ASCII'] = False
    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(index,url_prefix='/')
    app.register_blueprint(login,url_prefix='/login')
    app.register_blueprint(signin,url_prefix='/signin')
    app.register_blueprint(like,url_prefix='/like')
    app.register_blueprint(reset_password,url_prefix='/reset_password')
    app.register_blueprint(userprofile,url_prefix='/userprofile')
    app.register_blueprint(logout,url_prefix='/logout')
    app.register_blueprint(askque,url_prefix='/askque')
    app.register_blueprint(confirm_email,url_prefix='/confirm_email')
    app.register_blueprint(reset_link,url_prefix='/reset_link')
    app.register_blueprint(dislike,url_prefix='/dislike')
    app.register_blueprint(editprofile,url_prefix='/editprofile')
    app.register_blueprint(deletepost,url_prefix='/deletepost')
    app.register_blueprint(forum,url_prefix='/forum')
    app.register_blueprint(replay,url_prefix='/replay')
    return app
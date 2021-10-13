from flask import Flask, render_template, request, flash, redirect, url_for,make_response,session
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from datetime import datetime
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired,BadSignature
from flask_login import LoginManager,UserMixin, login_manager,logout_user,current_user,AnonymousUserMixin,login_user
from flask_login.utils import login_required
app = Flask(__name__)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=os.environ['EMAIL125']
app.config['MAIL_PASSWORD']=os.environ['PASSWORD125']
# app.config['MAIL_USERNAME']=''
# app.config['MAIL_PASSWORD']=''
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')
app.config['SECRET_KEY'] = 'hjhghg'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@localhost/flaskmovie'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'
app.secret_key = 'ye ye'
class User_Basic_infos(db.Model,UserMixin):
    __tablename__ = 'userbasicinfos'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    flags = db.Column(db.Boolean, default=False)
    usernamefull = db.Column(db.String,default="NOT_SET")
    Location = db.Column(db.String,default="NOT_SET")
    Bio = db.Column(db.String,default="NOT_SET")
    Image_Str = db.Column(db.String,default="1")
    Designation = db.Column(db.String,default="NOT_SET")
    phone = db.Column(db.String,default="NOT_SET")
    Instagram = db.Column(db.String,default="NOT_SET")
    Facebook = db.Column(db.String,default="NOT_SET")
    Twitter = db.Column(db.String,default="NOT_SET")
    Github = db.Column(db.String,default="NOT_SET")
    Linkdin = db.Column(db.String,default="NOT_SET")
    website = db.Column(db.String,default="NOT_SET")
    DOB = db.Column(db.Date,default='08-01-2003')

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"
class Forum_Questions(db.Model):
    __tablename__ = "forum_questions"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("userbasicinfos.id"))
    title = db.Column(db.String)
    discription = db.Column(db.String)
    time = db.Column(db.Date,default=datetime.now)
    def __repr__(self) -> str:
        return f"{self.id} - {self.user_id}"
class Forum_Questions_Reply(db.Model):
    __tablename__ = "forum_questions_replays"
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("userbasicinfos.id"))
    flag = db.Column(db.Integer)
    discription = db.Column(db.String)
    time = db.Column(db.Date,default=datetime.now)
    def __repr__(self) -> str:
        return f"{self.id} - {self.user_id}"
@login_manager.user_loader
def load_user(user_id):
    return User_Basic_infos.query.get(int(user_id))
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    global usn
    global psd
    global em
    if request.method == 'POST':
        try:
            usn = request.form['usn']
            psd = request.form['psd']
            em = request.form['em']
            just1 = User_Basic_infos(username=usn, password=psd, email=em,flags=False)
            db.session.add(just1)
            db.session.commit()
            coni = User_Basic_infos.query.filter_by(username=usn).first()
            token = s.dumps(em,salt='email-confirm')
            msg = Message('Hello',sender =os.environ['EMAIL125'],recipients = [em])
            link = url_for('confirm_email',token=token, id=coni.id,_external=True)
            msg.body = 'Your Token Is {}'.format(link)
            mail.send(msg)
            flash('Check Mail For Authentication')
            return render_template('index.html',flag=1)
        except:
            flash('Use Diffrent Username and Password')
            return render_template('index.html',flag=1)

    return render_template('index.html')

@app.route('/confirm_email/<token>/<int:id>')
def confirm_email(token,id):
    try:
        email = s.loads(token , salt='email-confirm',max_age=60)
        conf = User_Basic_infos.query.filter_by(id=id).first()
        conf.flags=True
        db.session.add(conf)
        db.session.commit()
    except SignatureExpired:
        return "The Token Is Expired"
    except BadSignature:
        return "The token is invalid"
    return "This email worked"
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        global eml
        global usnl
        usnl = request.form['usnl']
        psdl = request.form['psdl']
        eml = request.form['eml']
        try:
            cheking = User_Basic_infos.query.filter_by(username=usnl, password=psdl, email=eml,flags =True).first()
            if not cheking:
                flash('Username and Password Are Incorrect')
                return render_template('index.html',flag=2)
            else:
                login_user(cheking)
                session['visits']=cheking.id
                print("LOl",cheking.id)
                # resp = make_response()
                # resp.set_cookie('userID', cheking.id)
                # print("--->>>",request.cookies.get('userID'))
                # flash('login In Succesfully')
                user = User_Basic_infos.query.filter_by(id=session.get('visits')).first()
                return render_template('forums.html',user=user)
        except Exception as e:
            print(e)
            flash('Username and Password Are Incorrect')
            return render_template('index.html',flag=2)
    return render_template('index.html')
@app.route('/askque', methods=['GET','POST'])
@login_required
def askque():
    if request.method == 'POST':
        topic = request.form['tpc']
        Discription = request.form['tpcdisc']
        askingquestion = Forum_Questions(user_id=session.get('visits'),title=topic,discription=Discription)
        db.session.add(askingquestion)
        db.session.commit()
        user_profile = User_Basic_infos.query.filter_by(id=session.get('visits')).first()
    flash('Question Ask')
    return render_template('forums.html',flag =1,user = user_profile)
@app.route('/editprofile', methods=['GET','POST'])
@login_required
def editprofile(): 
    if request.method == 'POST':
        user_profile = User_Basic_infos.query.filter_by(id=session.get('visits')).first()
        # image_data = request.form.get("image_data")
        # text_data = request.form.get("text_data")
        # Location_data = request.form.get("Location_data")
        # Bio_data = request.form.get("Bio_data")
        # DOB_data = request.form.get("DOB_data")
        # Designation_data = request.form.get("Designation_data")
        image_data = request.form["imgsrc"]
        text_data = request.form["username"]
        Location_data = request.form["Location"]
        Bio_data = request.form["bio"]
        DOB_data = request.form["dob"]
        Designation_data = request.form["desig"]
        phone = request.form["Phone_Number"]
        Instagram = request.form["Instagram"]
        Facebook = request.form["Facebook"]
        Twitter = request.form["Twitter"]
        Github = request.form["Github"]
        Linkdin = request.form["Linkdin"]
        website = request.form["website"]
        user_profile.Image_Str = image_data
        user_profile.usernamefull = text_data
        user_profile.Location=Location_data
        user_profile.Bio=Bio_data
        user_profile.DOB=DOB_data
        user_profile.Designation=Designation_data
        user_profile.phone=phone
        user_profile.Instagram=Instagram
        user_profile.Facebook=Facebook
        user_profile.Twitter=Twitter
        user_profile.Github=Github
        user_profile.Linkdin=Linkdin
        user_profile.website=website
        db.session.add(user_profile)
        db.session.commit()
        print(image_data,text_data,Location_data,Bio_data,DOB_data,Designation_data)
        print("HEY THERE ITS WORKING YAYA")
        flash('Profile Edit Succesfully')
        return render_template('forums.html',flag =2,user = user_profile)
    user_profile = User_Basic_infos.query.filter_by(id=session.get('visits')).first()
    return render_template('forums.html',flag =20,user = user_profile)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Succesfully')
    return render_template('index.html',flag=1)
@app.route('/forum')
def forum():
    user =list(db.session.query(User_Basic_infos.Image_Str,User_Basic_infos.username)
                                .join(Forum_Questions, User_Basic_infos.id == Forum_Questions.user_id)
                                .all())
    forum_gg=Forum_Questions.query.all()
    lenghts=len(forum_gg)
    return render_template('test.html',ques=forum_gg,user=user,total_len=lenghts)
@app.route('/forum/<int:id>',methods=['GET','POST'])
def forum_id(id):
    forum_gg = Forum_Questions.query.filter_by(id=id).first()
    user =list(db.session.query(User_Basic_infos.Image_Str,User_Basic_infos.username)
                                .join(Forum_Questions, User_Basic_infos.id == forum_gg.user_id)
                                .first())
    replay = Forum_Questions_Reply.query.filter_by(flag=id).all()
    users =list(db.session.query(User_Basic_infos.Image_Str,User_Basic_infos.username)
                                .join(Forum_Questions_Reply, User_Basic_infos.id == Forum_Questions_Reply.user_id)
                                .all())
    print(user)
    return render_template('bbg.html',ques=forum_gg,user=user,replay=replay,users=users,lenghtsq=len(replay))

@app.route('/userprofile/<string:username>',methods=['GET','POST'])
def userprofile(username):
    if request.method == 'POST':
        user = User_Basic_infos.query.filter_by(username=username).first()
        if not user:
            return "Not Fund"
        return render_template('user_profile.html',user=user)
    user = User_Basic_infos.query.filter_by(username=username).first()
    if not user:
        return "Not Fund"
    return render_template('user_profile.html',user=user)

@app.route('/replay/<int:id>',methods=['GET','POST'])
def replay(id):
    if request.method == 'POST':
        comment = request.form["ncom"]
        replay_msg = Forum_Questions_Reply(user_id=session.get('visits'),flag=id,discription=comment)
        db.session.add(replay_msg)
        db.session.commit()
        print(comment)
        return forum_id(id)

if(__name__)=='__main__':
    app.run(debug=True)

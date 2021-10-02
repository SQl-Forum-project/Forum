from flask import Flask, render_template, request, flash, redirect, url_for,make_response,session
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
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
class Forumdg(db.Model,UserMixin):
    __tablename__ = 'forumdg7'
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
    DOB = db.Column(db.Date,default='08-01-2003')

    def __repr__(self) -> str:
        return f"{self.id} - {self.username}"
@login_manager.user_loader
def load_user(user_id):
    return Forumdg.query.get(int(user_id))
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
            just1 = Forumdg(username=usn, password=psd, email=em,flags=False)
            db.session.add(just1)
            db.session.commit()
            coni = Forumdg.query.filter_by(username=usn).first()
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
        conf = Forumdg.query.filter_by(id=id).first()
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
            cheking = Forumdg.query.filter_by(username=usnl, password=psdl, email=eml,flags =True).first()
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
                user = Forumdg.query.filter_by(id=session.get('visits')).first()
                return render_template('forums.html',user=user)
        except Exception as e:
            print(e)
            flash('Username and Password Are Incorrect')
            return render_template('index.html',flag=2)
    return render_template('index.html')
@app.route('/askque', methods=['GET','POST'])
@login_required
def askque():
    flash('Question Ask')
    return render_template('forums.html',flag =1)
@app.route('/editprofile', methods=['GET','POST'])
@login_required
def editprofile(): 
    if request.method == 'POST':
        user_profile = Forumdg.query.filter_by(id=session.get('visits')).first()
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
        user_profile.Image_Str = image_data
        user_profile.usernamefull = text_data
        user_profile.Location=Location_data
        user_profile.Bio=Bio_data
        user_profile.DOB=DOB_data
        user_profile.Designation=Designation_data
        db.session.add(user_profile)
        db.session.commit()
        print(image_data,text_data,Location_data,Bio_data,DOB_data,Designation_data)
        print("HEY THERE ITS WORKING YAYA")
        flash('Edit Profile')
        return render_template('forums.html',flag =2,user = user_profile)
    flash('Edit Profile')
    return render_template('forums.html',flag =2)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Succesfully')
    return render_template('index.html',flag=1)
@app.route('/test')
def test():
    return render_template('test.html')
@app.route('/userprofile/<string:username>')
@login_required
def userprofile(username):
    user = Forumdg.query.filter_by(username=username).first()
    if not user:
        return "Not Fund"
    return render_template('user_profile.html',user=user)

if(__name__)=='__main__':
    app.run(debug=True)
from model import db
from model.User import User
from flask import Blueprint, flash, render_template, request, session
from flask_login import login_required
editprofile = Blueprint(name="editprofile", import_name=__name__)


@editprofile.route('/', methods=['GET', 'POST'])
@login_required
def editprofiles():
    if request.method == 'POST':
        user_profile = User.query.filter_by(id=session.get('visits')).first()
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
        user_profile.Location = Location_data
        user_profile.Bio = Bio_data
        user_profile.DOB = DOB_data
        user_profile.Designation = Designation_data
        user_profile.phone = phone
        user_profile.Instagram = Instagram
        user_profile.Facebook = Facebook
        user_profile.Twitter = Twitter
        user_profile.Github = Github
        user_profile.Linkdin = Linkdin
        user_profile.website = website
        db.session.add(user_profile)
        db.session.commit()
        print(image_data, text_data, Location_data,
              Bio_data, DOB_data, Designation_data)
        print("HEY THERE ITS WORKING YAYA")
        flash('Profile Edit Succesfully')
        return render_template('forums.html', flag=2, user=user_profile)
    user_profile = User.query.filter_by(id=session.get('visits')).first()
    return render_template('forums.html', flag=20, user=user_profile)

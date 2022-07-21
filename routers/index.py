from flask import Blueprint,render_template
index = Blueprint(name="index", import_name=__name__)

@index.route('/')
def home():
    return render_template('index.html')
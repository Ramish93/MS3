import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)


@app.route('/')
@app.route('/index.html')
def index():
    user_info = mongo.db.user_info.find()
    return render_template('index.html', user_info=user_info)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        #checks if name exists in database
        name_exists = mongo.db.user_login.find_one(
            {'username': request.form.get('username').lower()})
    
        if name_exists:
            flash('User-Name already exists, please choose another name')
            return redirect (url_for('register'))

        register = {
            'username': request.form.get('username').lower(),
            'password': generate_password_hash(request.form.get('password'))
        }
        mongo.db.user_logins.insert_one(register)
        #puts new user into session
        session['user'] = request.form.get('username').lower() 
        flash('Registration was successful')
    return render_template("register.html")

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
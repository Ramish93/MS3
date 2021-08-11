import os
from flask import (
    Flask, flash, render_template, Response, make_response,
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # checks if name exists in database
        name_exists = mongo.db.user_logins.find_one(
            {'username': request.form.get('username').lower()})
 
        if name_exists:
            flash('User-Name already exists, please choose another name')
            return redirect(url_for('register'))

        register = {
            'username': request.form.get('username').lower(),
            'password': generate_password_hash(request.form.get('password'))
        }
        mongo.db.user_logins.insert_one(register)
        # puts new user into session
        session['user'] = request.form.get('username').lower() 
        flash('Registration was successful')
        return redirect(url_for('index', username=session['user']))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # checks if name exists
        name_exists = mongo.db.user_logins.find_one(
            {"username": request.form.get("username").lower()})

        if name_exists:
            # ensure hashed password matches user input
            if check_password_hash(
                name_exists["password"], request.form.get('password')):
                    session["user"] = request.form.get('username').lower()
                    flash('Welcome Again!')
                    return redirect(url_for('index', username=session['user']))
            else:
                # if invalid password
                flash('Incorrect Username and/or Password')
                return redirect(url_for("login"))

        else:
            # if name doesn't match
            flash('Incorrect Username and/or Password')
            return redirect(url_for('login'))

    return render_template("login.html")


@app.route('/')
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        user_data = {
            'first_name': request.form.get('first_name'),
            'last_name':request.form.get('last_name'),
            'dob': request.form.get('dob'),
            'email': request.form.get('email'),
            'education': request.form.get('education'),
            'skills': request.form.get('skills'),
            'experience': request.form.get('experience'),
            'linkdin': request.form.get('linkdin'),
            'about': request.form.get('about')
        }
        preview_user = mongo.db.user_info.insert(user_data)
        flash('Resume successfully saved and is ready for preview')
        print(preview_user)
        return redirect(url_for("cv_preview", user_info_id=preview_user))
    return render_template('index.html')


@app.route('/logout')
def logout():
    # removes session for user
    session.clear()
    flash("You're logged out")
    return redirect(url_for('login'))


@app.route("/cv_preview/<user_info_id>")
def cv_preview(user_info_id):
    preview = list(mongo.db.user_info.find({'_id': ObjectId(user_info_id)}))
    return render_template("cv_preview.html", preview=preview)


@app.route('/edit_info/<user_info_id>', methods=['GET', 'POST'])
def edit_info(user_info_id):
    if request.method == 'POST':
        info_update = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'dob': request.form.get('dob'),
            'email': request.form.get('email'),
            'education': request.form.get('education'),
            'skills': request.form.get('skills'),
            'experience': request.form.get('experience'),
            'linkdin': request.form.get('linkdin'),
            'about': request.form.get('about')
        }
        mongo.db.user_info.update({'_id': ObjectId(user_info_id)}, info_update)
        flash('Resume successfully updated')

    info = mongo.db.user_info.find_one({'_id': ObjectId(user_info_id)})

    return render_template("edit_info.html", info=info)


@app.route('/delet_info/<user_info_id>')
def delet_info(user_info_id):
    mongo.db.user_info.remove({'_id': ObjectId(user_info_id)})
    flash('Field successfully Deleted')
    return redirect(url_for('index'))


@app.route('/save_info/<user_info_id>')
def save_info(user_info_id):
    return redirect(url_for('index'))

# @app.route('/<first_name>/<last_name>/<dob>/<email>/<education>/<skills>/<experience>/<about>')
# def pdf_gen(first_name, last_name, dob,email, education, skills, experience, about):
#     render = render_template('cv_preview.html',first_name=first_name,
#         last_name=last_name,dob=dob, email=email, education=education,
#             skills=skills, experience=experience, about=about)

#     pdf = pdfkit.from_string(render, False)

#     responce = make_response(pdf)
#     responce.headers['content-type'] = 'application/pdf'
#     responce.headers['content-disposition'] = 'inline; filename = cv.pdf'

#     return responce

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)

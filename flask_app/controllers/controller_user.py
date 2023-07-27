from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.model_user import User
from flask_app.models.model_listing import Listing

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/')
    listings = Listing.get_all()
    user = User.get_one(session['user_id'])
    return render_template('dashboard.html', listings = listings, user=user)


@app.route('/user/create', methods=["POST"])
def user_create():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }
    user_id = User.write_user(data)
    print(user_id)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/user/login', methods =["POST"])
def login():
    data = {
        **request.form
    }
    user_in_db = User.login(data)
    if not user_in_db:
        flash("Invalid Email/Password", "error_users_login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "error_users_login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/api')
def api():
    return render_template('api.html')
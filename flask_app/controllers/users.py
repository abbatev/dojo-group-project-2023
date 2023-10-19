from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/')
def home():
    return redirect('/user/login')

@app.route('/user/login')
def login():
    if 'logged_in_id' in session:
        return redirect('/dashboard')
    return render_template('registration-login.html')


@app.route('/user/login/process', methods=['POST'])
def login_success():
    data = {
        "email": request.form['email']
    }
    user_from_db = User.get_by_email(data)
    if not user_from_db:
        flash('Email not found', "login")
        return redirect('/user/login')
    if not bcrypt.check_password_hash(user_from_db.password, request.form['password']):
        flash('Invalid Password', "login")
        return redirect('/login')
    session['logged_in_id'] = user_from_db.id
    return redirect('/dashboard')

@app.route('/user/register/process', methods=['POST'])
def register_success():
    if not User.validate_register(request.form):
        return redirect('/dashboard')
    else:
        data = {
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "email": request.form['email'],
                "password": bcrypt.generate_password_hash(request.form['password']),
                "created_at": request.form['created_at']
            }
        id = User.save(data)
        session['logged_in_id'] = id
    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
    if 'logged_in_id' in session:
        session.clear()
    return redirect('/user/login')

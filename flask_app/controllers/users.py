from flask_app import app
from flask import render_template, redirect, request, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
    user.User.save(data)
    print(data)
    return redirect('/dashboard')

@app.route('/user/login', methods=['POST'])
def login_user():
    data = {
        "email": request.form['email']
    }
    
    user_from_db = user.User.get_by_email(data)
    if not user_from_db:
        flash('Incorrect email')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_from_db, request.form['pwd']):
        flash('Invalid Login')
        return redirect('/login')
    return redirect('/dashboard')

@app.route('/dashboard')
def dash():
    return render_template('dash.html')



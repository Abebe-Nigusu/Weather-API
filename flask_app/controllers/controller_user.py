
from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.model_user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/subscribe')
def index():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():

    if not User.validator_user(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.create_user(data)
    session['user_id'] = id

    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_user_by_email(request.form)
    print('$$$$$$$$$$$$$$$$$$$$$$$', user)

    if not user:
        flash("Invalid Email", "login")
        return redirect('/subscribe')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/subscribe')

    session['user_id'] = user.id
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

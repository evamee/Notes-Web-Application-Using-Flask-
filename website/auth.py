 #route for login page
from flask import Flask,flash, Blueprint, render_template , request, redirect , url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,logout_user,login_required,current_user


auth = Blueprint("auth",__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')
    
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        FirstName = request.form.get('FirstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        # Check if the email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email is not valid.', category='error')
        elif len(FirstName) < 2:
            flash('First name must be greater than 1 character', category='error')  
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            # Create a new user
            new_user = User(email=email, FirstName=FirstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
    
    # Return a response for GET requests or unsuccessful POST requests
    return render_template('signup.html', user=current_user)


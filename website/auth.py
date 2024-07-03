from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash;
from . import db;
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in succesfully!', category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password!', category="error")
        else:
            flash('Email does not exist! Head to the Sign-up page',category='error')
                
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exists! Head to the Login page', category='error')
        elif len(email)==0:
            flash('You left some fields empty bub!', category='error')
        elif email.split('@')[1] !="gmail.com" and email.split('@')[1]!="outlook.com" and email.split('@')[1]!="yahoo.in" :
            flash("That ain't a valid address ", category='error')
        elif len(first_name) < 2:
            flash("It ain't nickname bub: First name's gotta be longer than 1 character", category='error')
        elif password1 != password2:
            flash('Bub... the passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('My grandma could crack that password: Make it longer than 7 characters at least.', category='error')
        else:
            new_user=User(email=email,firstName=first_name,password=generate_password_hash(password1,method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            user = User.query.filter_by(email=email).first()
            login_user(user,remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html",user=current_user)
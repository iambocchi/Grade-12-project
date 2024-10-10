from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('NAKALOGIN KANA!!!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('mali password mo dong, ulitin mo', category='error')
        else:
            flash('walang user na yan', category='error')

    return render_template("login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        userName = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        lrn = request.form.get('LRN')
        phoneNumber = request.form.get('phoneNumber')
        gender = request.form.get('genders')

        looklrn = User.query.filter_by(lrn=lrn).first()
        ifphoneexist = User.query.filter_by(phone_number=phoneNumber).first()
        user = User.query.filter_by(email=email).first()

        if user:
            flash('meron ng gantong user', category='error')
            # new added
        elif looklrn:
            flash('meron ng gantong LRN', category='error')
        elif not gender:
            flash('pick a gender.', category='error')
        
        elif len(lrn) < 5:
            flash('LRN must be greater than 5 characters.', category='error')

        elif ifphoneexist:
            flash('meron ng gantong phonenumber', category='error')

        elif len(phoneNumber) != 11:
            flash('phone number must be 11 characters.', category='error')


# end of new added
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(userName) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, userName=userName, password=generate_password_hash(password1, method='pbkdf2:sha256'), lrn=lrn, phone_number=phoneNumber, gender=gender)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))

    return render_template("sign_up.html", user=current_user)

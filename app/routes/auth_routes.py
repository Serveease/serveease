from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User
from datetime import datetime, date
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flask_mail import Message
from app import mail
from flask import Blueprint, render_template, request, flash, redirect, url_for
import os


auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', category='success')

            if user.role == 'admin':
                return redirect(url_for('admin.admin_home'))
            else:
                return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid credentials', category='danger')

    return render_template('login.html')

def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        barangay = request.form['barangay']
        district = request.form['district']
        birthday_str = request.form['birthday']
        gender = request.form['gender']
        phone = request.form['phone']
        civil_status = request.form['civil_status']

        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            age = calculate_age(birthday)
            if age < 13 or age > 120:
                flash("Only users aged between 13 and 120 can register.", "danger")
                return redirect(url_for('auth.register'))
        except ValueError:
            flash("Invalid birthday format.", "danger")
            return redirect(url_for('auth.register'))
        
        if not phone.startswith('09') and not phone.startswith('+639'):
            flash("Invalid phone number format.", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            barangay=barangay,
            district=district,
            birthday=birthday,
            gender=gender,
            phone=phone,
            civil_status=civil_status
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful.", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', category='info')
    return redirect(url_for('auth.login'))

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        from app.models import User
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = s.dumps(user.email, salt='password-reset')
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            
            msg = Message('Password Reset Request',
                          recipients=[user.email])
            msg.body = f'Click the link to reset your password: {reset_url}'
            
            # try:
            mail.send(msg)
            flash('A password reset link has been sent to your email.', 'success')
            # except Exception as e:
            #     flash('Error sending email. Please check your mail config.', 'danger')
        else:
            flash('No account found with that email.', 'warning')
    
    return render_template('auth/forgot_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form['password']
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash("Password updated successfully.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html')



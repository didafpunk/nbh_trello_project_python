from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from extensions import db
import hashlib
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from forms import LoginForm 
from forms import SignupForm 
from utils.password import verify_password 
auth_bp = Blueprint('auth', __name__)







@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        mail = form.mail.data
        password = form.password.data
        user = User.query.filter_by(mail=mail).first()
        if user and verify_password(password, user.password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Email ou mot de passe incorrect', 'error')
    return render_template('login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = SignupForm()
    if form.validate_on_submit():
        mail = form.mail.data
        fullname = form.fullname.data
        password = form.password.data
        
        # Vérifier si l'email existe déjà
        if User.query.filter_by(mail=mail).first():
            flash('Cet email est déjà utilisé', 'warning')
            return redirect(url_for('auth.signup'))
        
        hashed = generate_password_hash(password)
        user = User(mail=mail, fullname=fullname, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé, connectez-vous', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
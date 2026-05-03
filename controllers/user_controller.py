from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from forms import ProfileForm, ChangePasswordForm
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Vérification du mot de passe (hash MD5 salé)
def verify_password(plain, hashed):
    import hashlib
    prefix = "vJemLnU3"
    suffix = "QUaLtRs7"
    salted = prefix + plain + suffix
    computed = hashlib.md5(salted.encode()).hexdigest()
    return computed == hashed

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.fullname = form.fullname.data
        current_user.mail = form.mail.data
        db.session.commit()
        flash('Profil mis à jour', 'success')
        return redirect(url_for('user.profile'))
    return render_template('profile.html', form=form)

@user_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not verify_password(form.current_password.data, current_user.password):
            flash('Mot de passe actuel incorrect', 'error')
            return redirect(url_for('user.change_password'))
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Mot de passe modifié', 'success')
        return redirect(url_for('user.profile'))
    return render_template('change_password.html', form=form)
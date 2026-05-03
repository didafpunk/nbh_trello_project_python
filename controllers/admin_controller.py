from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from extensions import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Décorateur pour vérifier si l'utilisateur est admin
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != "admin":
            flash("Accès refusé. Vous n'êtes pas administrateur.", "danger")
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/users')
@admin_required
def list_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@admin_bp.route('/users/delete/<int:user_id>')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Vous ne pouvez pas supprimer votre propre compte.", "danger")
        return redirect(url_for('admin.list_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f"Utilisateur {user.fullname} supprimé avec succès.", "success")
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/users/toggle_admin/<int:user_id>')
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Vous ne pouvez pas modifier votre propre statut.", "danger")
        return redirect(url_for('admin.list_users'))
    
    # Basculer entre "user" et "admin"
    user.role = "admin" if user.role != "admin" else "user"
    db.session.commit()
    flash(f"Statut admin de {user.fullname} modifié.", "success")
    return redirect(url_for('admin.list_users'))
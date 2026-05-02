from flask import Flask, render_template, request, redirect, url_for
from models import db
import hashlib
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:@localhost/db_trello_project?connect_timeout=10"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 3600,
}

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


def verify_password(plain_password, hashed_password):
    prefix_salt = "vJemLnU3"
    suffix_salt = "QUaLtRs7"
    salted = prefix_salt + plain_password + suffix_salt
    computed_hash = hashlib.md5(salted.encode()).hexdigest()
    return computed_hash == hashed_password


@app.route("/signup", methods=["GET", "POST"])
def signup():
    from models import User

    if request.method == "POST":
        mail = request.form["mail"]
        fullname = request.form["fullname"]
        password = generate_password_hash(request.form["password"])

        new_user = User(mail=mail, fullname=fullname, password=password, role="user")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    from models import User

    if request.method == "POST":
        mail = request.form["mail"]
        password = request.form["password"]
        user = User.query.filter_by(mail=mail).first()

        if user and verify_password(password, user.password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return "Email ou mot de passe incorrect", 401

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return f"Bienvenue {current_user.fullname}, rôle : {current_user.role}"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)

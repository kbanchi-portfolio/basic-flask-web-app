import os

from dotenv import load_dotenv

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import jsonify
from flask import flash
from flask import url_for

from flask_cors import CORS

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from database import db
from database import User
from database import UserSchema
from database import Task
from database import TaskSchema

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from logger import get_logger

load_dotenv(verbose=True)

logger = get_logger()

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlalchemy.db"
# DB_USER = os.environ.get("DB_USER")
# DB_PASSWORD = os.environ.get("DB_PASSWORD")
# DB_HOST = os.environ.get("DB_HOST")
# DB_NAME = os.environ.get("DB_NAME")
# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = "mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8".format(
#     **{"user": DB_USER, "password": DB_PASSWORD, "host": DB_HOST, "db_name": DB_NAME}
# )
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get(
#     "SQLALCHEMY_TRACK_MODIFICATIONS"
# )
# app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO")
app.config["SECRET_KEY"] = os.urandom(24)

db.init_app(app)

with app.app_context():
    login_manager = LoginManager(app)
    db.drop_all()
    db.create_all()
    db.session.commit()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


@app.route("/healthcheck")
def healthcheck():
    return jsonify({"healthcheck": True})


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup_processing", methods=["POST"])
def signup_processing():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["passwd"]
    password_confirm = request.form["passwdConfirm"]
    if password != password_confirm:
        flash("Password confirm does not math.", "danger")
        return redirect(url_for("signup"))
    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists.", "danger")
        return redirect(url_for("signup"))
    generate_password_hash(
        password,
        method="pbkdf2",
    )
    db.session.add(
        User(
            name=name,
            email=email,
            password=generate_password_hash(
                password,
                method="pbkdf2",
            ),
        )
    )
    db.session.commit()
    flash("Create User", "success")
    return redirect(url_for("top"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_processing():
    email = request.form["email"]
    password = request.form["passwd"]
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("top"))
    flash("Email or Password does not match.", "danger")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/top")
def top():
    return render_template("top.html")


@app.route("/")
def index():
    return redirect("/top")


@app.route("/add")
@login_required
def add():
    return render_template("add_task.html")


@app.route("/edit")
@login_required
def edit():
    return render_template("edit_task.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = True if os.environ.get("ENV") == "local" else False
    app.run(host="0.0.0.0", port=port, debug=debug)

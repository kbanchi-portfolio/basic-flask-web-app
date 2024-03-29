import os

from dotenv import load_dotenv

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import jsonify
from flask import flash
from flask import url_for
from flask import session

from flask_cors import CORS

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from flask_babel import Babel
from flask_babel import gettext

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


LANGUAGES = ["ja", "ja_JP", "en"]


def get_locale():
    # return request.accept_languages.best_match(['ja', 'ja_JP', 'en'])
    # return request.args.get("lang") if request.args.get("lang") in LANGUAGES else None
    return session["lang"] if session["lang"] in LANGUAGES else None


app = Flask(__name__)
CORS(app)
babel = Babel(app, locale_selector=get_locale)

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
    if os.environ.get("DB_INIT") == "init":
        db.drop_all()
        db.create_all()
    db.session.commit()


@app.before_request
def initialize_session():
    if "lang" not in session:
        session["lang"] = "en"


@app.before_request
def switch_language():
    if "lang" in request.args:
        if request.args.get("lang") in LANGUAGES:
            session["lang"] = request.args.get("lang")


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("top"))


@app.route("/healthcheck")
def healthcheck():
    return jsonify({"healthcheck": True})


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_processing():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["passwd"]
    password_confirm = request.form["passwdConfirm"]
    if password != password_confirm:
        flash(gettext("password_confirm_not_match"), "danger")
        return redirect(url_for("signup"))
    user = User.query.filter_by(email=email).first()
    if user:
        flash(gettext("email_address_already_exists"), "danger")
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
    flash(gettext("complete_create_user"), "success")
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
    flash(gettext("email_or_password_does_not_match"), "danger")
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
def index():
    return redirect(url_for("top"))


@app.route("/top")
@login_required
def top():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("top.html", tasks=tasks)


@app.route("/add")
@login_required
def add():
    return render_template("add_task.html")


@app.route("/add", methods=["POST"])
@login_required
def add_processing():
    description = request.form["description"]
    db.session.add(
        Task(
            user_id=current_user.id,
            description=description,
        )
    )
    db.session.commit()
    flash(gettext("complete_create_task"), "success")
    return redirect(url_for("top"))


@app.route("/edit/<id>")
@login_required
def edit(id):
    task = Task.query.filter_by(id=id).first()
    return render_template("edit_task.html", task=task)


@app.route("/edit/<id>", methods=["POST"])
@login_required
def edit_processing(id):
    method = request.form.get("_method", "").upper()
    if method == "PUT":
        task = Task.query.filter_by(id=id).first()
        task.description = request.form["description"]
        flash(gettext("complete_edit_task"), "success")
        db.session.commit()
    elif method == "DELETE":
        task = Task.query.filter_by(id=id).delete()
        flash(gettext("complete_delete_task"), "danger")
        db.session.commit()
    return redirect(url_for("top"))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = True if os.environ.get("ENV") == "local" else False
    app.run(host="0.0.0.0", port=port, debug=debug)

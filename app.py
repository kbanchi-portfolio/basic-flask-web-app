import os

from dotenv import load_dotenv

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import jsonify

from flask_cors import CORS

from database import db
from database import User
from database import UserSchema
from database import Task
from database import TaskSchema

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
# app.config["SECRET_KEY"] = os.urandom(24)

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()

@app.route("/healthcheck")
def healthcheck():
    return jsonify({"healthcheck": True})


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    return render_template("login.html")

@app.route("/top")
def top():
    return render_template("top.html")

@app.route("/")
def index():
    return redirect("/top")

@app.route("/add")
def add():
    return render_template("add_task.html")

@app.route("/edit")
def edit():
    return render_template("edit_task.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = True if os.environ.get("ENV") == "local" else False
    app.run(host="0.0.0.0", port=port, debug=debug)

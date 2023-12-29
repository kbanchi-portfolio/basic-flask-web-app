import os

from dotenv import load_dotenv

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import jsonify

from flask_cors import CORS

from logger import get_logger

load_dotenv(verbose=True)

logger = get_logger()

app = Flask(__name__)
CORS(app)

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

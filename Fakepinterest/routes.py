# criar as rotas do site
from flask import render_template, url_for
from Fakepinterest import app
from flask_login import login_required

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/user/<user>")
@login_required
def userpage(user):
    return render_template("user/user.html", user=user)
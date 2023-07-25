# criar as rotas do site
from flask import render_template, url_for
from Fakepinterest import app

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/user/<user>")
def userpage(user):
    return render_template("user/user.html", user=user)
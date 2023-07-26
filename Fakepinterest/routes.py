from flask import render_template, url_for
from Fakepinterest import app
from Fakepinterest.forms import FormLogin, FormSingUp
from flask_login import login_required

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    return render_template("homepage.html", form=formlogin)

@app.route("/singup", methods=["GET", "POST"])
def singup():
    formSingUp = FormSingUp()
    return render_template("singup.html", form=formSingUp)

@app.route("/user/<user>")
@login_required
def userpage(user):
    return render_template("user/user.html", user=user)
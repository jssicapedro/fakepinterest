from flask import render_template, url_for, redirect
from Fakepinterest import app, database, bcrypt
from Fakepinterest.models import User, Post
from Fakepinterest.forms import FormLogin, FormSingUp, FormPhoto
from flask_login import login_required, login_user, logout_user, current_user
import os
import secrets
from werkzeug.utils import secure_filename

@app.route("/", methods=["GET", "POST"])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        user = User.query.filter_by(email=formlogin.email.data).first()
        if user and bcrypt.check_password_hash(user.password, formlogin.password.data):
            login_user(user)
            return redirect(url_for("userpage", id_user=user.id))
    return render_template("homepage.html", form=formlogin)

@app.route("/singup", methods=["GET", "POST"])
def singup():
    form_SingUp = FormSingUp()
    if form_SingUp.validate_on_submit():
        password = bcrypt.generate_password_hash(form_SingUp.password.data)
        user = User(
            name=form_SingUp.name.data,
            email=form_SingUp.email.data,
            password=password
        )
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("userpage", id_user=user.id))
    return render_template("singup.html", form=form_SingUp)

@app.route("/user/<id_user>", methods=["GET", "POST"])
@login_required
def userpage(id_user):
    if int(id_user) == int(current_user.id):
        form_photo = FormPhoto()
        if form_photo.validate_on_submit():
            file = form_photo.photo.data
            extension = os.path.splitext(file.filename)[1]  # Obtém a extensão do arquivo
            random_name = secrets.token_hex(16) + extension  # Gera um nome aleatório
            name_file = secure_filename(random_name)

            # guardar imagem na pasta
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], name_file)
            file.save(path)

            # registo de imagem na BD
            image = Post(image=name_file, id_user=current_user.id)
            database.session.add(image)
            database.session.commit()
        return render_template("user/user.html", user=current_user, form=form_photo)
    else:
        user = User.query.get(int(id_user))
        return render_template("user/user.html", user=user, form=None)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route("/feed")
def feed():
    return render_template("feed.html")
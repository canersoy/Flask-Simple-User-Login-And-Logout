from app import app, db
from flask import render_template, request, flash, redirect, url_for, session, abort
from app.forms import LoginForm, SignupForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User


@app.route("/", methods=["GET", "POST"])
def initPage():
    loginForm = LoginForm()
    if loginForm.loginButton.data and loginForm.validate():
        usernameOrEmail = request.form["usernameOrEmail"]
        password = request.form["password"]
        print(User.query.filter_by(username=usernameOrEmail).first())
        if not(User.query.filter_by(username=usernameOrEmail).first() is None):
            user = User.query.filter_by(username=usernameOrEmail).first()
        else:
            user = User.query.filter_by(email=usernameOrEmail).first()
        if user and check_password_hash(user.password, password):
            session[usernameOrEmail] = True
            flash("Successfully logged in.")
            return redirect(url_for("userPage", usernameOrEmail=usernameOrEmail))
        else:
            flash("Invalid username or password.")

    signupForm = SignupForm()
    if signupForm.signupButton.data and signupForm.validate():
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password, 'sha256')
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("User account has been created.")
        return redirect(url_for("initPage"))
    return render_template("initPage.html", loginForm=loginForm, signupForm=signupForm)


@app.route("/user/<usernameOrEmail>/")
def userPage(usernameOrEmail):
    if not session.get(usernameOrEmail):
        abort(401)
    return render_template("userPage.html",usernameOrEmail=usernameOrEmail)


@app.route("/logout/<usernameOrEmail>")
def logout(usernameOrEmail):
    session.pop(usernameOrEmail, None)
    flash("Successfully logged out.")
    return redirect(url_for("initPage"))

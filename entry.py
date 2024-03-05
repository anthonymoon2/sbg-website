from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from models import db, users
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

entry = Blueprint("entry", __name__, static_folder="static", template_folder="templates-entry")

@entry.route("/login", methods=["POST", "GET"])
def login():
  session.pop('_flashes', None) # clear flash messages
  if request.method == "POST":
    email = request.form['email'].lower()
    password = request.form.get("password")
    found_user = users.query.filter_by(email=email).first()

    if found_user:
      if check_password_hash(found_user.password, password):
        flash("Login Successful.", "success")
        login_user(found_user, remember=True)
        # Check the account type and redirect accordingly
        if found_user.accountType == 'Teacher':
          return redirect(url_for("teacherClass.teacherHome"))
        else:  # Assume other account types are students for now
          return redirect(url_for("studentClass.studentHome"))
      else:
        flash("Incorrect password.", "error")
    else:
        flash("An account with this email does not exist!", "error")
  return render_template("login.html")

@entry.route("/signup", methods=["POST", "GET"])
def signup():
  if request.method == 'POST':
    email = request.form.get("email").lower()
    name = request.form.get('name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    accountType = request.form.get('accountType')

    if not all([email, name, password1, password2, accountType]):
      flash("Please fill in all fields!", "error")
      return render_template("signup.html")

    user = users.query.filter_by(email=email).first()
    if user:
      flash('Email already exists.', "error")
    elif len(email) < 4:
      flash('Email must be greater than 3 characters', "error")
    elif len(name) < 1:
      flash('First name must be greater than 1 character', "error")
    elif password1 != password2:
      flash('Passwords don\'t match.', "error")
    elif len(password1) < 7:
      flash('Password must be at least 7 characters', "error")

    else:
      new_user = users(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'), accountType=accountType)
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash('Account created!', "success")
      return redirect(url_for('entry.login'))
  return render_template("signup.html")

@entry.route("/logout")
@login_required
def logout():
  logout_user()
  flash('Logged out', "success")
  return redirect(url_for('entry.login'))




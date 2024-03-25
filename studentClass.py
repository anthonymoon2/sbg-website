from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from models import db, schoolClasses, users, StudentClassAssociation

studentClass = Blueprint("studentClass", __name__, static_folder="static", template_folder="templates-student")

def user_is_authenticated():
  return current_user.is_authenticated and hasattr(current_user, 'id')

@login_required
@studentClass.route("/studentHome")
def studentHome():
  if user_is_authenticated():
    studentClasses = current_user.classes  # retrieve all classes 
    return render_template("studenthome.html", name=current_user.name, classes=studentClasses)
  else:
    flash("You are not logged in!")
    return redirect(url_for("entry.login"))

@studentClass.route("/studentProfile")
def studentProfile():
  if user_is_authenticated():
    return render_template("studentProfile.html", name=current_user.name, email=current_user.email)
  else:
    flash("You are not logged in!")
    return redirect(url_for("entry.login"))

@studentClass.route("/studentAssignments")
def studentAssignments():
  if user_is_authenticated():
    return render_template("studentAssignments.html")
  else:
    flash("You are not logged in!")
    return redirect(url_for("entry.login"))
  
@studentClass.route("/class/<int:class_id>")
def classPageHome(class_id):
  selectedClass = schoolClasses.query.get_or_404(class_id)
  return render_template("classPageHome.html", selectedClass=selectedClass)

@studentClass.route("/class/<int:class_id>/assignments")
def classPageAssignments(class_id):
  selectedClass = schoolClasses.query.get_or_404(class_id)
  return render_template("classPageAssignments.html", selectedClass=selectedClass)

@studentClass.route("/class/<int:class_id>/students", methods=['GET', 'POST'])
def classPageStudents(class_id):
  selectedClass = schoolClasses.query.get_or_404(class_id)
  listCurrStudents = users.query.join(StudentClassAssociation, users.id == StudentClassAssociation.student_id).filter(StudentClassAssociation.class_id == class_id).all()

  return render_template("classPageStudents.html", allCurrentStudents=listCurrStudents, selectedClass=selectedClass)
  
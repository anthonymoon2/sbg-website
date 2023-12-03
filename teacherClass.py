from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from models import db, schoolClasses, users, StudentClassAssociation, assignment

teacherClass = Blueprint("teacherClass", __name__, static_folder="static", template_folder="templates-teacher")

def user_is_teacher():
  return current_user.is_authenticated and hasattr(current_user, 'accountType') and current_user.accountType == 'Teacher'

@login_required
@teacherClass.route("/teacherHome")
def teacherHome():
  classes = schoolClasses.query.filter_by(teacher=current_user.id).all()
  return render_template("teacherHome.html", user=current_user, schoolClasses=classes)

@teacherClass.route("/teacherProfile")
def teacherProfile():
  if user_is_teacher():
    return render_template("teacherProfile.html", name=current_user.name, email=current_user.email)
  else:
    flash("Access denied: You do not have permission to view this page.")
    return redirect(url_for("entry.login"))

@teacherClass.route("/teacherClassManagement", methods=['GET', 'POST'])
def teacherClassManagement():
  if not user_is_teacher():
    flash("Access denied: You do not have permission to view this page.")
    return redirect(url_for("entry.login"))

  if request.method == 'POST':
    action = request.form.get('action')

    if action == 'addClass':
      teacherClass = request.form.get('schoolClass')
      if teacherClass is None or len(teacherClass) < 1:
        flash('Class name is too short!')
      else: 
        new_class = schoolClasses(className=teacherClass, teacher=current_user.id)
        db.session.add(new_class)
        db.session.commit()
        flash('New class added!')

    elif action == 'deleteClass':
      classToDeleteID = request.form.get("classIdToDelete")
      classToDelete = schoolClasses.query.get(classToDeleteID)

      if classToDelete:
        db.session.delete(classToDelete)
        db.session.commit()
        flash('Class deleted successfully.')
      else:
        flash('Class not found.')
        
  classes = schoolClasses.query.filter_by(teacher=current_user.id).all()
  return render_template("teacherClassManagement.html", user=current_user, schoolClasses=classes)


@teacherClass.route("/class/<int:class_id>")
def classPageHomeT(class_id):
  selectedClass = schoolClasses.query.get_or_404(class_id)
  return render_template("classPageHomeT.html", selectedClass=selectedClass)

@teacherClass.route("/class/<int:class_id>/assignments", methods=['GET', 'POST'])
def classPageAssignmentsT(class_id):
  selectedClass = schoolClasses.query.get_or_404(class_id)

  if request.method == "POST":
    action = request.form.get('action')

    if action == "addAssignment":
      assignment_name = request.form.get('classAssignmentName')
      new_assignment = assignment(name=assignment_name, class_id=class_id)
      db.session.add(new_assignment)
      db.session.commit()
      return redirect(url_for('teacherClass.classPageAssignmentsT', class_id=class_id))
    
    elif action == "deleteAssignment":
      assignment_id_to_delete = request.form.get('assignmentIdToDelete')
      if assignment_id_to_delete:
        assignment_id_to_delete = int(assignment_id_to_delete)
        assignment_to_delete = assignment.query.get(assignment_id_to_delete)
        if assignment_to_delete:
          db.session.delete(assignment_to_delete)
          db.session.commit()
    return redirect(url_for('teacherClass.classPageAssignmentsT', class_id=class_id))
  
  assignments = assignment.query.filter_by(class_id=class_id).all()
  return render_template("classPageAssignmentsT.html", selectedClass=selectedClass, assignments=assignments)


@teacherClass.route("/class/<int:class_id>/students", methods=['GET', 'POST'])
def classPageStudentsT(class_id):
  selectedClass = schoolClasses.query.get_or_404(class_id)

  if request.method == "POST":
    action = request.form.get('action')

    # when the teacher clicks add student
    if action == "addStudentToClass":
      currentStudent = request.form.get('studentIdToAdd') # get the chosen student ID
      studentEnrollmentCheck = StudentClassAssociation.query.filter_by(student_id=currentStudent, class_id=class_id).first()
      if studentEnrollmentCheck is None: 
        # student is not in the class
        enrollment = StudentClassAssociation(student_id=currentStudent, class_id=class_id)
        db.session.add(enrollment)
        db.session.commit()
        flash("Student added successfully!")
      else:
        flash("Student is already enrolled in this class.", "warning")

    # when the teacher clicks delete student
    elif action == "deleteStudentFromClass":
      currentStudent = request.form.get('studentIdToDelete')  # get the chosen student ID
      
      studentEnrollmentCheck = StudentClassAssociation.query.filter_by(student_id=currentStudent, class_id=class_id).first()
      
      if studentEnrollmentCheck:
        db.session.delete(studentEnrollmentCheck)
        db.session.commit()
        flash("Student deleted from class successfully.")
      else:
        flash("Student is not enrolled in this class.")

  listStudents = users.query.filter_by(accountType="Student").all()
  listCurrStudents = users.query.join(StudentClassAssociation, users.id == StudentClassAssociation.student_id).filter(StudentClassAssociation.class_id == class_id).all() 

  return render_template("classPageStudentsT.html", selectedClass=selectedClass, allStudents=listStudents, allCurrentStudents=listCurrStudents)
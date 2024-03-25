from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Association table for the many-to-many relationship
class StudentClassAssociation(db.Model):
  __tablename__ = 'student_class_association'
  student_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
  class_id = db.Column(db.Integer, db.ForeignKey('schoolClasses.id'), primary_key=True)

class users(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  accountType = db.Column(db.String(150))
  # Relationship to link users with classes
  classes = db.relationship('schoolClasses', secondary='student_class_association', back_populates="students")

class schoolClasses(db.Model):
  __tablename__ = 'schoolClasses'
  id = db.Column(db.Integer, primary_key=True)
  className = db.Column(db.String(10000))
  teacher = db.Column(db.Integer, db.ForeignKey('users.id'))
  # Relationship to link classes with users
  students = db.relationship('users', secondary='student_class_association', back_populates="classes")
  assignments = db.relationship('assignment', back_populates="class_")

class assignment(db.Model):
  __tablename__ = 'assignments'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(1000))
  class_id = db.Column(db.Integer, db.ForeignKey('schoolClasses.id'))

  # Relationship to link assignment with a class
  class_ = db.relationship('schoolClasses', back_populates="assignments")
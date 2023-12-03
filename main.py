from flask import Flask, render_template
from flask_login import LoginManager
from datetime import timedelta
from models import db, users

from entry import entry
from studentClass import studentClass
from teacherClass import teacherClass

app = Flask(__name__)
app.register_blueprint(entry, url_prefix="/entry")
app.register_blueprint(studentClass, url_prefix='/student')
app.register_blueprint(teacherClass, url_prefix='/teacher')

app.secret_key = "moon"
app.permanent_session_lifetime = timedelta(days=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'entry.login' 

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route("/")
def homebase():
    return render_template("homebase.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


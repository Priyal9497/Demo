from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask, render_template, request


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

@app.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        employee = Employee(
            name=request.form["name"],
            email=request.form["email"],
            department=request.form["department"],
            salary=request.form["salary"]
        )

        db.session.add(employee)
        db.session.commit()

        return "Employee Added Successfully"

    return render_template("add_employee.html")
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        employee = Employee(
            name=request.form["name"],
            email=request.form["email"],
            department=request.form["department"],
            salary=request.form["salary"]
        )

        db.session.add(employee)
        db.session.commit()

        return "Employee Added Successfully"

    return render_template("add_employee.html")
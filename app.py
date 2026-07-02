from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


# -----------------------------
# Database Model
# -----------------------------
class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Employee {self.name}>"


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# View Employees
# -----------------------------
@app.route("/employees")
def employees():

    search = request.args.get("search")

    if search:
        employee_list = Employee.query.filter(
            Employee.name.ilike(f"%{search}%")
        ).all()
    else:
        employee_list = Employee.query.order_by(Employee.id.desc()).all()

    return render_template(
        "employees.html",
        employees=employee_list
    )


# -----------------------------
# Add Employee
# -----------------------------
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

        return redirect(url_for("employees"))

    return render_template("add_employee.html")


# -----------------------------
# Edit Employee
# -----------------------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    employee = Employee.query.get_or_404(id)

    if request.method == "POST":

        employee.name = request.form["name"]
        employee.email = request.form["email"]
        employee.department = request.form["department"]
        employee.salary = request.form["salary"]

        db.session.commit()

        return redirect(url_for("employees"))

    return render_template(
        "edit_employee.html",
        employee=employee
    )


# -----------------------------
# Delete Employee
# -----------------------------
@app.route("/delete/<int:id>")
def delete_employee(id):

    employee = Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    return redirect(url_for("employees"))


# -----------------------------
# Create Database
# -----------------------------
with app.app_context():
    db.create_all()


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
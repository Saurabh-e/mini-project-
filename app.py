from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",        # change if different
    password="saurabh@121",  # change
    database="employee_db"
)
cursor = db.cursor(dictionary=True)

# Home (Login Page)
@app.route('/')
def home():
    return render_template("login.html")

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        department = request.form['department']
        role = request.form['role']

        cursor.execute("INSERT INTO employees (name,email,password,department,role) VALUES (%s,%s,%s,%s,%s)",
                       (name, email, password, department, role))
        db.commit()
        flash("Signup successful! Please login.", "success")
        return redirect('/')
    return render_template("signup.html")

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cursor.execute("SELECT * FROM employees WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        return redirect('/dashboard')
    else:
        flash("Invalid email or password!", "danger")
        return redirect('/')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template("dashboard.html", employees=employees)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "waste123"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="waste_management"
)

cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        sql = "SELECT * FROM users WHERE email=%s AND password=%s"
        values = (email, password)

        cursor.execute(sql, values)
        user = cursor.fetchone()

        if user:
            session["email"] = email
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        fullname = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        sql = "INSERT INTO users (fullname, email, phone, password) VALUES (%s, %s, %s, %s)"
        values = (fullname, email, phone, password)

        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/complaint", methods=["GET", "POST"])
def complaint():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        location = request.form["location"]
        waste_type = request.form["type"]
        description = request.form["description"]

        # IMAGE UPLOAD PART
        image = request.files["image"]

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        sql = """
        INSERT INTO complaints
        (name, email, location, waste_type, description, status, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (name, email, location, waste_type, description, "Pending", filename)

        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for("success"))

    return render_template("complaint.html")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid Admin Login"

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():

    # All complaints
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    # Total complaints
    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    # Pending complaints
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    # Resolved complaints
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    return render_template(
        "admin_dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        resolved=resolved
    )

@app.route("/update_status/<int:id>")
def update_status(id):

    sql = "UPDATE complaints SET status='Resolved' WHERE id=%s"

    cursor.execute(sql, (id,))
    db.commit()

    return redirect(url_for("admin_dashboard"))
@app.route("/delete_complaint/<int:id>")
def delete_complaint(id):

    sql = "DELETE FROM complaints WHERE id=%s"

    cursor.execute(sql, (id,))
    db.commit()

    return redirect(url_for("admin_dashboard"))
@app.route("/my_complaints")
def my_complaints():

    email = session.get("email")

    cursor.execute(
        "SELECT * FROM complaints WHERE email=%s",
        (email,)
    )

    complaints = cursor.fetchall()

    return render_template(
        "my_complaints.html",
        complaints=complaints
    )
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)
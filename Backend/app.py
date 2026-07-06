from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "waste123"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("waste_management.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

db = get_db()
cursor = db.cursor()

# Tables illaina create pannum (first run la mattum)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    location TEXT,
    waste_type TEXT,
    description TEXT,
    status TEXT,
    image TEXT
)
""")
db.commit()

print("✅ Database Connected Successfully")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        sql = "SELECT * FROM users WHERE email=? AND password=?"
        cursor.execute(sql, (email, password))
        user = cursor.fetchone()

        if user:
            session["email"] = email
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing = cursor.fetchone()

        if existing:
            return "Email already registered. Please login."

        sql = """
        INSERT INTO users(fullname,email,phone,password)
        VALUES(?,?,?,?)
        """

        cursor.execute(sql, (fullname, email, phone, password))
        db.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- COMPLAINT ----------------
@app.route("/complaint", methods=["GET", "POST"])
def complaint():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        location = request.form["location"]
        waste_type = request.form["type"]
        description = request.form["description"]

        image = request.files["image"]

        filename = secure_filename(image.filename)

        image.save(
            os.path.join(app.config["UPLOAD_FOLDER"], filename)
        )

        sql = """
        INSERT INTO complaints
        (name,email,location,waste_type,description,status,image)
        VALUES(?,?,?,?,?,?,?)
        """

        values = (
            name,
            email,
            location,
            waste_type,
            description,
            "Pending",
            filename
        )

        cursor.execute(sql, values)
        db.commit()

        return redirect(url_for("success"))

    return render_template("complaint.html")

# ---------------- SUCCESS ----------------
@app.route("/success")
def success():
    return render_template("success.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- PROFILE ----------------
@app.route("/profile")
def profile():
    return render_template("profile.html")


# ---------------- REPORTS ----------------
@app.route("/reports")
def reports():
    return render_template("reports.html")


# ---------------- CONTACT ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- ADMIN LOGIN ----------------
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


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():

    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]

    return render_template(
        "admin_dashboard.html",
        complaints=complaints,
        total=total,
        pending=pending,
        resolved=resolved
    )


# ---------------- UPDATE STATUS ----------------
@app.route("/update_status/<int:id>")
def update_status(id):

    cursor.execute(
        "UPDATE complaints SET status='Resolved' WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect(url_for("admin_dashboard"))


# ---------------- DELETE COMPLAINT ----------------
@app.route("/delete_complaint/<int:id>")
def delete_complaint(id):

    cursor.execute(
        "DELETE FROM complaints WHERE id=?",
        (id,)
    )

    db.commit()

    return redirect(url_for("admin_dashboard"))

# ---------------- MY COMPLAINTS ----------------
@app.route("/my_complaints")
def my_complaints():

    email = session.get("email")

    if not email:
        return redirect(url_for("login"))

    cursor.execute(
        "SELECT * FROM complaints WHERE email=?",
        (email,)
    )

    complaints = cursor.fetchall()

    return render_template(
        "my_complaints.html",
        complaints=complaints
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
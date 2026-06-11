from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Waste Management System"

@app.route('/login')
def login():
    return "Login Page"

@app.route('/dashboard')
def dashboard():
    return "Dashboard Page"

if __name__ == '__main__':
    app.run(debug=True)

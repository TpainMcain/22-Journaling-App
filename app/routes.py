from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.models import User, Journal
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize LoginManager with the app instance.
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirects users to the login page when they try to access a @login_required route without being logged in.

# This function is used by Flask-Login to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registration route.
@app.route("/register", methods=["GET", "POST"])
def register():
    # If the user is already logged in, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Register a new user.
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

# Login route.
@app.route("/login", methods=["GET", "POST"])
def login():
    # If the user is already logged in, redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # User login functionality.
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

# Logout route.
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# Journal route for users to post journal entries.
@app.route("/journal", methods=["GET", "POST"])
@login_required  # User must be logged in to access this route.
def journal():
    if request.method == "POST":
        prompt = "Your random prompt for today"  # This can be fetched from a list of prompts
        content = request.form.get('content')
        journal_entry = Journal(prompt=prompt, content=content, author=current_user)
        db.session.add(journal_entry)
        db.session.commit()
        flash('Your journal entry has been saved!', 'success')
        return redirect(url_for('home'))
    return render_template('journal.html')

# Home route.
@app.route('/')
def home():
    return render_template('base.html')

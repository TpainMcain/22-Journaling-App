# app/routes.py

from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.models import User, Journal
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/journal", methods=["GET", "POST"])
@login_required
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

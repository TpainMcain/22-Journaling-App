# Import necessary libraries and modules
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from app.models import User, Journal
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirects users to the login page if they attempt to access a page where login is required.

@login_manager.user_loader
def load_user(user_id):
    """Reload the user object from the user ID stored in the session."""
    return User.query.get(int(user_id))

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
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/journal", methods=["GET", "POST"])
@login_required
def journal():
    categories = [
        "Emotions", 
        "Dreams", 
        "Future Goals", 
        "Past Memories", 
        "Travel",
        "Relationships",
        "Personal Growth",
        "Daily Activities",
        "Creative Ideas",
        "Health & Wellness"
    ]

    prompts = [
        ["How do you feel today", "When were you last angry", "Describe a joyful moment", "Whats weighing on your mind"],
        ["Describe a recent dream", "Have you had recurring dreams", "Dreams or reality", "A dream place you wish to visit"],
        ["Where do you see yourself in 5 years", "Whats a skill youd like to learn", "List down your top 3 future goals", "How will you achieve them"],
        ["Recall a fond childhood memory", "A mistake you learned from", "Describe a day youd like to relive"],
        ["Your dream travel destination", "A memorable trip you had", "Traveling solo or with companions", "Describe a local hidden gem"],
        ["Describe a meaningful conversation you had recently", "How have your relationships evolved", "Someone youre grateful for", "A lesson learned from a relationship"],
        ["A moment you felt immense growth", "Whats a recent challenge you overcame", "What are your current barriers to growth"],
        ["How did you spend your day", "Something unexpected that happened", "A simple joy from today", "What are you looking forward to tomorrow"],
        ["A project youd like to start", "Describe a hobby youd like to pursue", "Whats an idea that excites you"],
        ["What are your current health goals", "How do you feel physically today", "Whats a new healthy habit youve adopted", "Discuss a recent wellness activity you tried"]
    ]
    
    if request.method == "POST":
        prompt = request.form.get('selected_prompt', "Your random prompt for today")
        content = request.form.get('content')
        journal_entry = Journal(prompt=prompt, content=content, author=current_user)
        db.session.add(journal_entry)
        db.session.commit()
        flash('Your journal entry has been saved!', 'success')
        return redirect(url_for('home'))
    
    return render_template('journal.html', categories=categories, prompts=prompts)

@app.route('/')
def home():
    return render_template('base.html')

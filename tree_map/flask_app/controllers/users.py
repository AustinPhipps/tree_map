from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.tree import Tree
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    users_id = User.save(data)

    session['user_id'] = users_id

    return redirect('/dashboard')

@app.route('/login_user', methods=['POST'])
def login_user():
    data = {
        'email' : request.form['email']
    }

    user_in_db = User.get_one_by_email(data)
    
    if not user_in_db:
        flash('Invalid email or password.')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash('Invalid email or password.')
        return redirect('/')
    
    session['users_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'users_id' not in session:
        flash('Please log in.')
        return redirect('/')

    all_trees = Tree.get_all_w_creator()

    
    return render_template('dashboard.html', all_trees=all_trees)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
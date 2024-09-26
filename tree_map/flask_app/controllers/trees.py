from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.tree import Tree

@app.route('/tree_form')
def tree_form():
    return render_template('tree_form.html')

@app.route('/add_tree', methods=['POST'])
def add_tree():
    data = {
        'species' : request.form['species'],
        'location' : request.form['location'],
        'date' : request.form['date'],
        'zip' : request.form['zip'],
        'notes' : request.form['notes'],
        'users_id' : session['users_id']
    }

    if not Tree.validate_tree(request.form):
        return redirect('/tree_form')

    Tree.save_tree(data)
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def view(id):

    data = {
        'id' : id
    }

    tree = Tree.get_one_by_id(data)

    user = Tree.get_tree_info(data)

    if 'users_id' not in session:
        flash('Please log in.')
        return redirect('/')

    return render_template('show.html', tree=tree, user=user)

@app.route('/edit/<int:id>')
def update_form(id):

    data = {
        'id' : id
    }

    tree = Tree.get_one_by_id(data)

    if 'users_id' not in session:
        flash('Please log in.')
        return redirect('/')
    
    return render_template('edit.html', tree=tree)

@app.route('/edit/<int:id>', methods=['POST'])
def update_tree(id):
    data = {
        'id' : id,
        'species' : request.form['species'],
        'location' : request.form['location'],
        'date' : request.form['date'],
        'zip' : request.form['zip'],
        'notes' : request.form['notes']
    }

    if not Tree.validate_tree(request.form):
        return redirect('/dashboard')

    Tree.update(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_tree(id):
    data = {
        'id' : id
    }

    Tree.delete(data)

    return redirect('/dashboard')
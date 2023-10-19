from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.comment import Comment
from flask_app.models.user import  User
from flask_app.models.listing import Listing

@app.route('/dashboard')
def dashboard():
    if 'logged_in_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['logged_in_id']})
    # comment = Comment.get_comments_for_listings(comment)
    listings = Listing.get_all()
    return render_template('dashboard.html', user=user, all_listings=listings)

@app.route('/listings/new')
def create_listing():
    if 'logged_in_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['logged_in_id']})
    return render_template('create_listing.html', user=user)

@app.route('/listings/new/process', methods=['POST'])
def add_listing():
    if 'logged_in_id' not in session:
        return redirect('/user/login')
    if not Listing.validate_listing(request.form):
        return redirect('/listings/new')
    data = {
        'make_model': request.form['make_model'],
        'year': request.form['year'],
        'condition': request.form['condition'],
        'price': request.form['price'],
        'mileage' : request.form['mileage'],
        'description': request.form['description'],
        'created_at':request.form['created_at'],
        'user_id': session['logged_in_id']
    }
    Listing.save(data)
    return redirect('/dashboard')

@app.route('/listings/show/<int:id>' , methods=['GET'])
def show_listing(id):
    if 'logged_in_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['logged_in_id']})
    listing = Listing.get_by_id({'id': id})
    return render_template('listing.html', user=user, listing=listing)

@app.route('/listings/edit/<int:id>')
def edit_listing(id):
    user = User.get_by_id({"id":session['logged_in_id']})
    listing = Listing.get_by_id({'id': id})
    if 'logged_in_id' not in session:
        return redirect('/user/login')
    elif user.id != listing.user_id:
        return redirect('/dashboard')
    else:
        return render_template('edit_listing.html', user=user , listing=listing)

@app.route('/listings/edit/process/<int:id>', methods=['POST'])
def update_listing(id):
    if 'logged_in_id' not in session:
        return redirect('/user/login')
    if not Listing.validate_listing(request.form):
        return redirect(f'/listings/edit/{id}')
    data = {
        'id': id,
        'make_model': request.form['make_model'],
        'year': request.form['year'],
        'condition': request.form['condition'],
        'price': request.form['price'],
        'mileage' : request.form['mileage'],
        'description': request.form['description'],
        'updated_at':request.form['updated_at'],
    }
    Listing.update(data)
    return redirect('/dashboard')

@app.route('/listings/delete/<int:id>')
def delete_listing(id):
    listing = Listing.get_by_id({'id':id})
    user = User.get_by_id({"id":session['logged_in_id']})
    if 'logged_in_id' not in session:
        return redirect('/user/login')
    elif user.id != listing.user_id:
        return redirect('/dashboard')
    else:
        Listing.destroy({'id': id})
        return redirect('/dashboard')

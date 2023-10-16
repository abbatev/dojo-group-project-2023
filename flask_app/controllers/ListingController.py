from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_app.models.comment import Comment
from flask_app.models.user import  User
from flask_app.models.listing import Listing 
from flask_app.config.mysqlconnection import connectToMySQL

app = Flask(__name__)


@app.route('/Dash')
def Dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    comment = Comment.get_comments_for_listings(comment)
    listing = Listing.get_all()
    return render_template('dash.html',  comment=comment, user=user, listing=listing , users_id=user.id)


@app.route('/view/<make_model>' , methods=['GET'])
def viewOne(make_model):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    listing = Listing.get_by_name(make_model)
    return render_template('one.html', user=user, listing=listing)

@app.route('/create/listing')
def createOneForm():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    return render_template('create-listing.html', user=user)


@app.route('/update/listing' , methods=['POST', 'GET'])
def UpdateListingForm():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    listing = Listing.get_by_id(session['user_id'])
    return render_template('edit.html', user=user , listing=listing)

@app.route('/delete_listing/<int:users_id>', methods=['POST'])
def delete_listing(users_id):
    listing = Listing.get_by_id(users_id)
    if listing is not None and listing.users_id == session['user_id']:
        Listing.destroy(users_id)
    return redirect(url_for('dash'))


@app.route('/listing/save', methods=['POST'])
def add_listing():
    if not Listing.validate_listing(request.form):
        return redirect('/create/listing')
    data = {
        'make_model': request.form['make_model'],
        'year': request.form['year'],
        'listing_condition': request.form['listing_condition'],
        'price': request.form['price'],
        'milage' : request.form['milage'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'created_at':request.form['created_at'],
        'updated_at':request.form['updated_at'],
        'users_id': session['user_id'],

    }
    Listing.save(data)
    return redirect(url_for('dash'))

@app.route('/edit/listing/<int:users_id>', methods=['GET', 'POST'])
def update_listing(users_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.get_by_id(session['user_id'])
    listing = Listing.get_by_id(users_id)
    if listing is None or listing.users_id != user.id:
        return redirect(url_for('dash'))
    if request.method == 'POST':
        if not Listing.validate_listing(request.form):
            return redirect(url_for('edit', users_id=users_id))
        data = {
                'make_model': request.form['make_model'],
                'year': request.form['year'],
                'listing_condition': request.form['listing_condition'],
                'price': request.form['price'],
                'milage' : request.form['milage'],
                'description': request.form['description'],
                'instruction': request.form['instruction'],
                'created_at':request.form['created_at'],
                'updated_at':request.form['updated_at'],
                'users_id': session['user_id'],
                }
        Listing.update(users_id, data)
        return redirect(url_for('dash', name=listing.name))
    return render_template('edit.html', user=user,  listing=listing)


if __name__ == "__main__":
    app.run(debug=True)
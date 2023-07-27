from flask_app import app
from flask import render_template, redirect, request, session, flash
import base64

from flask_app.models.model_listing import Listing
from flask_app.models.model_user import User


@app.route('/listing/new')
def listing_new():
    if 'user_id' not in session:
        return redirect ('/')
    return render_template("new_listing.html")

@app.route('/listing/show')
def listing_show():
    user = User.get_one(session['user_id'])
    return render_template("show_listing.html", user=user)


listings = []
@app.route('/listing/create', methods=['POST', 'GET'])
def listing_create():
    image = request.files['photo']
    base64_encoded = base64.b64encode(image.read())
    # .decode("utf-8")
    data = {
        **request.form,
        "photo": base64_encoded
    }
    if not Listing.validate_listing(request.form):
        return redirect('/listing/new')
    listing = Listing.create(data)
    return redirect('/dashboard')


@app.route('/listing/<int:id>/delete')
def listing_delete(id):
    Listing.delete_one(id)
    return redirect('/dashboard')


@app.route('/listing/<int:id>/show')
def show_listing(id):
    listing = Listing.get_one(id)
    return render_template("show_listing.html", listing = listing)


@app.route('/listing/<int:id>/edit')
def edit_listing(id):
    listing = Listing.get_one(id)
    return render_template("edit_listing.html", listing = listing)



@app.route('/listing/<int:id>/update', methods=['POST'])
def update_listing(id):
    data = {
        **request.form
    }
    data["id"] = id
    if not Listing.validate_listing(request.form):
        return redirect('/listing/<int:id>/edit')
    Listing.update(data)
    return redirect('/dashboard')



from flask import Blueprint, redirect, render_template, request, flash, url_for, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.database import db
from App.models.upload import Upload
from App.controllers.upload import remove_file
from App.models import Apartment, Review, User, Landlord, Tenant
from App.controllers.apartment import (
    create_apartment,
    get_all_apartments,
    get_apartment_by_id,
    update_apartment,
    delete_apartment,
    search_apartment
)

apartment_views = Blueprint('apartment_views', __name__, template_folder='../templates')

# CREATE Apartment
@apartment_views.route('/apartments/new', methods=['GET', 'POST'])
@jwt_required()
def new_apartment():
    if request.method == 'POST':
        landlord_id = get_jwt_identity()
        form_data = request.form.to_dict()
        photo_file = request.files.get('photo')

        # Handle file upload
        if photo_file and photo_file.filename:
            upload = Upload(photo_file)
            db.session.add(upload)
            form_data['photo'] = upload.filename
        else:
            form_data['photo'] = 'Image not available'

        create_apartment(form_data, landlord_id)
        flash('Apartment added successfully!')
        return redirect(url_for('index_views.index_page'))


# UPDATE Apartment
@apartment_views.route('/apartments/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required()
def edit_apartment(id):
    apartment = get_apartment_by_id(id)
    if not apartment:
        flash('Apartment not found.')
        return redirect(url_for('index_views.index_page'))

    if request.method == 'POST':
        form_data = request.form.to_dict()
        photo_file = request.files.get('photo')

        if photo_file and photo_file.name:

            if apartment.photo and apartment.photo != 'Image not available':
                try:
                   remove_file(apartment.photo) # function defined in upload controller
                except:
                    print('Could not delete old photo')

            upload=Upload(photo_file)
            db.session.add(upload)
            form_data['photo']=upload.filename # filename is an existing function 

        else:
            form_data['photo'] = apartment.photo    # this prevents the upload from being overwritten by nothing when editing 

        update_apartment(id, form_data)
        flash('Apartment updated successfully!')
        return redirect(url_for('index_views.index_page'))


# DELETE Apartment
@apartment_views.route('/apartments/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_apartment_route(id):
    review=Review.query.filter_by(apartment_id=id).all()

    for rev in review:
        db.session.delete(rev)

    if  delete_apartment(id):
        flash('Apartment deleted.')
    else:
        flash('Apartment not found.')
    return redirect(url_for('index_views.index_page'))

#SEARCH BY LOCATION OR AMENITIES 
@apartment_views.route('/apartments/search' , methods=['GET'])
@jwt_required()
def search_apartment_route():
      search_value=request.args
      if(search_value):
        found=search_apartment(search_value)
      else:
          found=None
      
      return render_template('index.html',found=found)

# @apartment_views.route('/apartments/<int:id>', methods=['GET'])
# @jwt_required()
# def show_apartments(id):
#     apartments = Apartment.query.all()

#     selected_apartment = get_apartment_by_id(id)
#     print("selected_id:",id)
#     #selected_apartment = Apartment.query.get(selected_id) if selected_id else None

#     reviews = []
#     if selected_apartment:
#         reviews = Review.query.filter_by(apartment_id=selected_apartment.id).all()

#     return render_template(
#         'index.html',
#         apartments=apartments,
#         selected_apartment=selected_apartment,
#         reviews=reviews,
#         user_id=session.get('user_id'),
#         user_type=session.get('user_type')
#     )
@apartment_views.route('/apartments/<int:id>', methods=['GET'])
@jwt_required()
def show_apartments(id):
    apartments = Apartment.query.all()


    selected_apartment = get_apartment_by_id(id)
    print("selected_id:", id)

    reviews = []
    if selected_apartment:
        reviews = Review.query.filter_by(apartment_id=selected_apartment.id).all()

   
    user_reviews = []
    if session.get('user_id') and session.get('user_type') == 'tenant':
        user_reviews = Review.query.filter_by(tenant_id=session.get('user_id')).all()

    return render_template(
        'index.html',
        apartments=apartments,
        selected_apartment=selected_apartment,
        reviews=reviews,
        user_id=session.get('user_id'),
        user_type=session.get('user_type'),
        user_reviews=user_reviews 
    )

from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.database import db
from App.models.upload import Upload
from App.controllers.upload import remove_file
from App.controllers.apartment import (
    create_apartment,
    get_all_apartments,
    get_apartment_by_id,
    update_apartment,
    delete_apartment
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

    return render_template('add_apartment.html')

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
            form_data['photo']='file not uploaded in edit' # to be safe
        
        update_apartment(id, form_data)
        flash('Apartment updated successfully!')
        return redirect(url_for('index_views.index_page'))

    return render_template('edit_apartment.html', apartment=apartment)

# DELETE Apartment
@apartment_views.route('/apartments/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_apartment_route(id):
    if delete_apartment(id):
        flash('Apartment deleted.')
    else:
        flash('Apartment not found.')
    return redirect(url_for('index_views.index_page'))

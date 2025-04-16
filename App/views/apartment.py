from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.database import db

from App.controllers.apartment import (
    create_apartment,
    get_all_apartments,
    get_apartment_by_id,
    update_apartment,
    delete_apartment
)

apartment_views = Blueprint('apartment_views', __name__, template_folder='../templates')

@apartment_views.route('/apartments/new', methods=['GET', 'POST'])
@jwt_required()
def add_apartment():
    if request.method == 'POST':
        landlord_id = get_jwt_identity()
        create_apartment(request.form, landlord_id)
        flash('Apartment added successfully!')
        return redirect(url_for('index_views.index_page'))
    return render_template('add_apartment.html')


@apartment_views.route('/apartments/<int:id>/edit', methods=['GET', 'POST'])
@jwt_required()
def edit_apartment(id):
    apartment = get_apartment_by_id(id)
    if not apartment:
        flash('Apartment not found.')
        return redirect(url_for('index_views.index_page'))

    if request.method == 'POST':
        update_apartment(id, request.form)
        flash('Apartment updated successfully!')
        return redirect(url_for('index_views.index_page'))

    return render_template('edit_apartment.html', apartment=apartment)


@apartment_views.route('/apartments/<int:id>/delete', methods=['POST'])
@jwt_required()
def delete_apartment_route(id):
    if delete_apartment(id):
        flash('Apartment deleted.')
    else:
        flash('Apartment not found.')
    return redirect(url_for('index_views.index_page'))
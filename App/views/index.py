from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, session
from App.controllers import create_user, initialize
from App.controllers.apartment import get_all_apartments
from App.models import Apartment, Landlord, Tenant, Review

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', endpoint='index_page')
def home():
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    
    apartments = Apartment.query.all()  # for the main list in column 1

    user_apartments = []
    user_reviews = []

    if user_id and user_type == 'landlord':
        landlord = Landlord.query.get(user_id)
        if landlord:
            user_apartments = landlord.apartments

    elif user_id and user_type == 'tenant':
        tenant = Tenant.query.get(user_id)
        if tenant:
            user_reviews = tenant.reviews

    return render_template(
        'index.html',
        apartments=apartments,
        user_id=user_id,
        user_type=user_type,
        user_apartments=user_apartments,  # for editing/deleting
        user_reviews=user_reviews         # for editing/deleting
    )

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, session
from App.controllers import create_user, initialize
from App.controllers.apartment import get_all_apartments
from App.models import Apartment, Landlord, Tenant, Review
from App.controllers.apartment import search_apartment

index_views = Blueprint('index_views', __name__, template_folder='../templates')


# Route for the index page
@index_views.route('/app', endpoint='index_page')
def home():
    user_id = session.get('user_id')
    user_type = session.get('user_type')

    if not user_id or not user_type:
        return redirect('/')  
    
    apartments = Apartment.query.all() 

    user_apartments = []
    user_reviews = []

    if user_type == 'landlord':
        landlord = Landlord.query.get(user_id)
        if landlord:
            user_apartments = landlord.apartments

    elif user_type == 'tenant':
        tenant = Tenant.query.get(user_id)
        if tenant:
            user_reviews = tenant.reviews

    return render_template(
        'index.html',
        apartments=apartments,
        user_id=user_id,
        user_type=user_type,
        user_apartments=user_apartments,
        user_reviews=user_reviews
    )
 

 #Route to initialize the database
@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')


#Route to check health of the application
@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})
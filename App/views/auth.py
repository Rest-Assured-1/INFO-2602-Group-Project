from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies

from App.controllers import login
from App.models import User, Tenant, Landlord
from App.database import db

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = User.query.all()
    return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")


@auth_views.route('/', methods=['GET', 'POST'])
def login_action():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.form
    username = data['username']
    password = data['password']

    token = login(username, password)
    response = redirect('/app')

    if not token:
        flash('Bad username or password given')
        return render_template('login.html')
    else:
        flash('Login Successful')
        set_access_cookies(response, token)

        # ✅ Instead of current_user, directly look up user by username
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id  # Now safe to use
            session['user_type'] = user.user_type

    return response



@auth_views.route('/signup', methods=['GET', 'POST'])
def signup_action():
    if request.method == 'GET':
        return render_template('signup.html')

    data = request.form
    username = data['username']
    password = data['password']
    user_type = data['user_type']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists')
        return redirect(url_for('auth_views.signup_action'))

    if user_type == 'tenant':
        user = Tenant(username=username, password=password)
    elif user_type == 'landlord':
        user = Landlord(username=username, password=password)
    else:
        user = User(username=username, password=password)

    db.session.add(user)
    db.session.commit()
    flash('Signup successful! Please login.')
    return redirect(url_for('auth_views.login_action'))


@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('auth_views.login_action'))
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response


@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
    data = request.json
    token = login(data['username'], data['password'])
    if not token:
        return jsonify(message='bad username or password given'), 401
    response = jsonify(access_token=token)
    set_access_cookies(response, token)
    return response


@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response

from App.models import User, Landlord, Tenant
from App.database import db


#Function to create new users
def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser


#Function to create new landlords
def create_landlord(username, password):
    newuser = Landlord(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser


#Function to create new tenants
def create_tenant(username, password):
    newuser = Tenant(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

#Function to get users by username
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


#Function to get users by id
def get_user(id):
    return User.query.get(id)


#Function to get all users
def get_all_users():
    return User.query.all()


#Function to get all landlords
def get_all_landlords():
    return Landlord.query.all()


#Function to get all users in json format
def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users


#Function to update user information
def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    
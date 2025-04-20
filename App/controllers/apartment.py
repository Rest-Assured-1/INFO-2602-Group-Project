from App.models import Apartment
from App.database import db
from flask import url_for

def create_apartment(data, landlord_id):
    apartment = Apartment(
        title=data.get('title'),
        body=data.get('body'),
        amenities=data.get('amenities'),
        photo=data.get('photo'),
        pets_allowed=data.get('pets_allowed'),
        price=float(data.get('price')),
        address=data.get('address'),
        cityname=data.get('cityname'),
        landlord_id=landlord_id
    )
    db.session.add(apartment)
    db.session.commit()
    return apartment

def get_all_apartments():
    return Apartment.query.all()

def get_apartment_by_id(apartment_id):
    return Apartment.query.get(apartment_id)

def update_apartment(apartment_id, data):
    apartment = get_apartment_by_id(apartment_id)
    if not apartment:
        return None
    apartment.title = data.get('title')
    apartment.body = data.get('body')
    apartment.amenities = data.get('amenities')
    apartment.photo = data.get('photo')
    apartment.pets_allowed = data.get('pets_allowed')
    apartment.price = float(data.get('price'))
    apartment.address = data.get('address')
    apartment.cityname = data.get('cityname')
    db.session.commit()
    return apartment

def delete_apartment(apartment_id):
    apartment = get_apartment_by_id(apartment_id)
    if not apartment:
        return False
    db.session.delete(apartment)
    db.session.commit()
    return True

def search_apartment(data):
    value=data.get('value','').lower()
    apartments=None
    if value!="":
         apartments=db.session.query(Apartment).filter(db.or_(Apartment.amenities.ilike(f'%{ value }%'), Apartment.cityname.ilike(f'%{value}%' ))).all()
    else:
        apartments=Apartment.query
    return apartments
    


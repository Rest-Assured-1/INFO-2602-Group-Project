from App.models import Apartment
from App.database import db

def create_apartment(title, body, amenities, photo, pets_allowed, price, address, cityname, landlord_id):
    apartment = Apartment(
        title=title,
        body=body,
        amenities=amenities,
        photo=photo,
        pets_allowed=pets_allowed,
        price=price,
        address=address,
        cityname=cityname,
        landlord_id=landlord_id
    )
    db.session.add(apartment)
    db.session.commit()

def get_apartment_by_id(apartment_id):
    return Apartment.query.get(apartment_id)

def get_all_apartments():
    return Apartment.query.all()
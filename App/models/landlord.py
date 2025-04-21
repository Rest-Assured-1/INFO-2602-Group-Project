from .user import User
from App.database import db
from .apartment import Apartment


class Landlord(User):
    __tablename__ = 'landlord'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'landlord',
    }


    def __init__(self, username, password):
        super().__init__(username, password)


    def __repr__(self):
        return f'<Landlord {self.id} {self.username}>'


    def create_apartment(self, title, body, price, address, photo, city, amenities, pets_allowed):
        try:
            apartment = Apartment(
                landlord_id=self.id,
                title=title,
                body=body,
                price=price,
                address=address,
                photo=photo,
                cityname=city,
                pets_allowed=pets_allowed,
                amenities=amenities
            )
            db.session.add(apartment)
            db.session.commit()
            return apartment
        except Exception as e:
            print('Error creating apartment:', e)
            db.session.rollback()
            return None


    def delete_apartment(self, apartment):
        try:
            apartment.status = 'delisted'
            db.session.commit()
            return True
        except Exception as e:
            print('Error deleting apartment:', e)
            db.session.rollback()
            return False


    def update_apartment(self, apartment, title=None, body=None, price=None, address=None, city=None, amenities=None, pets_allowed=None):
        try:
            if title:
                apartment.title = title
            if body:
                apartment.body = body
            if price:
                apartment.price = price
            if address:
                apartment.address = address
            if city:
                apartment.cityname = city
            if amenities:
                apartment.amenities = amenities
            if pets_allowed is not None:
                apartment.pets_allowed = pets_allowed

            db.session.commit()
            return apartment
        except Exception as e:
            print('Error updating apartment:', e)
            db.session.rollback()
            return None


    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'type': 'landlord',
            'listings': [apt.toJSON() for apt in self.apartments]
        }

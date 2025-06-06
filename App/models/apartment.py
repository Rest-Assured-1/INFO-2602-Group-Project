from App.database import db
from flask import url_for


class Apartment(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    amenities = db.Column(db.String(200), nullable=True)
    photo = db.Column(db.String(200), nullable=True)
    pets_allowed = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float)
    address = db.Column(db.String(200))
    cityname = db.Column(db.String(100))
   
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlord.id'))

    landlord = db.relationship('Landlord', backref=db.backref('apartments', lazy='joined'))


    def __repr__(self):
        return f'<Apartment {self.id} {self.title}>'


    def toJSON(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'amenities': self.amenities,
            'photo': self.photo,
            'pets_allowed': self.pets_allowed,
            'price': self.price,
            'address': self.address,
            'cityname': self.cityname,
            'landlord_id': self.landlord_id
        }

    @property
    def photo_url(self):
        if self.photo and (self.photo.startswith('http') or self.photo.startswith('https')):
            return self.photo
        elif self.photo:
            return url_for('upload_views.uploaded_file', filename=self.photo)
    
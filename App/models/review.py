from App.database import db
from datetime import datetime


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    tenant = db.relationship('Tenant', backref='reviews', lazy='joined')
    apartment = db.relationship('Apartment', backref=db.backref('reviews', lazy='joined'))

    def __init__(self, tenant_id, apartment_id, rating, comment=None):
        self.tenant_id = tenant_id
        self.apartment_id = apartment_id
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f'<Review {self.id} {self.rating} by Tenant {self.tenant_id} for Apartment {self.apartment_id}>'

    def toJSON(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'apartment_id': self.apartment_id,
            'rating': self.rating,
            'comment': self.comment,
        }

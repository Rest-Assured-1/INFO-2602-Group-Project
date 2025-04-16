from .user import User
from App.database import db

class Tenant(User):
    __tablename__ = 'tenant'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'tenant',
    }

    def __init__(self, username, password):
        super().__init__(username, password)

    def __repr__(self):
        return f'<Tenant {self.id} {self.username}>'

    def get_reviews(self):
        return self.reviews

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'type': 'tenant',
            'reviews': [review.toJSON() for review in self.reviews] 
        }

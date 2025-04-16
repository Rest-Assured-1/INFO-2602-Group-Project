from App.models import Review, Apartment
from App.database import db
from flask_login import current_user

def add_review(apartment_id, rating, content):
    apartment = Apartment.query.get(apartment_id)
    if apartment:
        new_review = Review(
            content=content,
            rating=rating,
            apartment_id=apartment.id,
            tenant_id=current_user.id 
        )
        db.session.add(new_review)
        db.session.commit()


def get_reviews_for_apartment(apartment_id):
    return Review.query.filter_by(apartment_id=apartment_id).all()

def update_review(review_id, rating, content):
    review = Review.query.get(review_id)
    if review and review.tenant_id == current_user.id:
        review.rating = rating
        review.content = content
        db.session.commit()

def delete_review(review_id):
    review = Review.query.get(review_id)
    if review and review.tenant_id == current_user.id:
        db.session.delete(review)
        db.session.commit()


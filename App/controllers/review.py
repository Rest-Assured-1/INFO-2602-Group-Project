from App.models import Review, Apartment
from App.database import db

def create_review(apartment_id, rating, content, tenant_id):
    apartment = Apartment.query.get(apartment_id)

    if apartment:
        new_review = Review(
            content=content,
            rating=rating,
            apartment_id=apartment.id,
            tenant_id=tenant_id
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review


def get_reviews_for_apartment(apartment_id):
    return Review.query.filter_by(apartment_id=apartment_id).all()


def update_review(review_id, rating, content):
    review = Review.query.get(review_id)
    if not review:
        return None
    
    review.rating = rating
    review.content = content
    db.session.commit()
    return review


def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return False
    db.session.delete(review)
    db.session.commit()
    return True

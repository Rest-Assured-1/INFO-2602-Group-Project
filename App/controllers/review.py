from App.models import Review, Apartment
from App.database import db

#Function to create a review for an apartment
def create_review(apartment_id, rating, comment, tenant_id):
    apartment = Apartment.query.get(apartment_id)

    if apartment:
        new_review = Review(
            comment=comment,
            rating=rating,
            apartment_id=apartment.id,
            tenant_id=tenant_id
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review


# Function to get all reviews for an apartment
def get_reviews_for_apartment(apartment_id):
    return Review.query.filter_by(apartment_id=apartment_id).all()


#Function to update a review for an apartment
def update_review(review_id, rating, comment):
    review = Review.query.get(review_id)
    if not review:
        return None
    
    review.rating = rating
    review.comment = comment
    db.session.commit()
    return review


#Function to delete a review for an apartment
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return False
    db.session.delete(review)
    db.session.commit()
    return True

from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.database import db
from App.controllers.review import (
    create_review, 
    get_reviews_for_apartment, 
    update_review, 
    delete_review
)
from App.models import Apartment, Review

review_views = Blueprint('review_views', __name__, template_folder='../templates')


@review_views.route('/apartments/<int:apartment_id>/reviews', methods=['GET'])
@jwt_required()
def view_reviews(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)
    reviews = get_reviews_for_apartment(apartment_id)
    return render_template('view_reviews.html', apartment=apartment, reviews=reviews)



@review_views.route('/apartments/<int:apartment_id>/reviews/add', methods=['GET', 'POST'])
@jwt_required()
def add_review(apartment_id):
    apartment = Apartment.query.get_or_404(apartment_id)

    if request.method == 'POST':
        tenant_id = get_jwt_identity()
        rating = request.form.get('rating')
        comment = request.form.get('comment')

        if rating and comment:
            create_review(apartment_id, rating, comment, tenant_id)
            flash('Review added successfully!', 'success')
            return redirect(url_for('review_views.view_reviews', apartment_id=apartment.id))
        else:
            flash('Please provide both rating and comment!', 'error')

    return render_template('add_review.html', apartment=apartment)


@review_views.route('/reviews/<int:review_id>/edit', methods=['GET', 'POST'])
@jwt_required()
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)

    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        if rating and comment:
            update_review(review_id, rating, comment)
            flash('Review updated successfully!', 'success')
            return redirect(url_for('review_views.view_reviews', apartment_id=review.apartment_id))
        else:
            flash('Please provide both rating and comment!', 'error')

    return render_template('edit_review.html', review=review)


@review_views.route('/reviews/<int:review_id>/delete', methods=['POST'])
@jwt_required()
def delete_review_route(review_id):
    review = Review.query.get_or_404(review_id)

    delete_review(review_id)
    flash('Review deleted successfully!', 'success')
    return redirect(url_for('review_views.view_reviews', apartment_id=review.apartment_id))

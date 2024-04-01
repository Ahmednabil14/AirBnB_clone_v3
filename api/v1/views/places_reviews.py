#!/usr/bin/python3
"""reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_place_reviews(place_id):
    """Retrieves the list of all reviews objects of a place"""
    reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        for review in storage.all(Review).values():
            if review.place_id == place_id:
                reviews.append(review.to_dict())
        return jsonify(reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """get a review"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route(
    "/reviews/<review_id>",
    methods=["DELETE"],
    strict_slashes=False)
def delete_review(review_id):
    """delete review"""
    review = storage.get(Review, review_id)
    response = jsonify({})
    response.status_code = 200
    if review:
        storage.delete(review)
        storage.save()
        return (response)
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>/reviews",
    methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """create review"""
    data = request.get_json(force=True, silent=True)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data.keys():
        return jsonify({"error": "Missing user_id"}), 400
    found = 0
    for user in storage.all(User).values():
        if user.id == data["user_id"]:
            found = 1
            break
    if found == 0:
        abort(404)
    if 'text' not in data.keys():
        return jsonify({"error": "Missing text"}), 400
    review = Review(user_id=data["user_id"], text=data["text"])
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """update review"""
    data = request.get_json(force=True, silent=True)
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key in data.keys():
        if key not in [
            "id", "user_id", "place_id", "created_at", "updated_at"
                ]:
            setattr(review, key, data[key])
    review.save()
    storage.save()
    return jsonify(review.to_dict()), 200

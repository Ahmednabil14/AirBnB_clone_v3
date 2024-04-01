#!/usr/bin/python3
""" places_amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t


@app_views.route("/places/<uuid:place_id>/amenities",
                 methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """place_amenities route"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if storage_t == 'db':
        amenities = place.amenities
    else:
        amenities = [storage.get('Amenity', id)
                     for id in place.amenity_ids]
    amenities = list(map(lambda x: x.to_dict(), amenities))
    return jsonify(amenities)


@app_views.route("/places/<uuid:place_id>/amenities/<uuid:amenity_id>",
                 methods=['DELETE', 'POST'],
                 strict_slashes=False)
def place_amenity(place_id, amenity_id):
    """place_amenity route"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)
    if place is None or amenity is None:
        abort(404)
    if storage_t == 'db':
        if request.method == 'DELETE':
            if amenity not in place.amenities:
                abort(404)
            storage.delete(amenity)
            place.amenities.remove(amenity)
            storage.save()
            return jsonify({})
        else:  # POST
            if amenity in place.amenities:
                return jsonify(amenity.to_dict())
            else:
                place.amenities.append(amenity)
                storage.save()
                return jsonify(amenity.to_dict()), 201
    else:
        if request.method == 'DELETE':
            if amenity.id not in place.amenity_ids:
                abort(404)
            storage.delete(amenity)
            place.amenity_ids.remove(amenity.id)
            storage.save()
            return jsonify({})
        else:  # POST
            if amenity.id in place.amenity_ids:
                return jsonify(amenity.to_dict())
            else:
                place.amenity_ids.append(amenity.id)
                storage.save()
                return jsonify(amenity.to_dict()), 201

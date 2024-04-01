#!/usr/bin/python3
""" amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities():
    """amenities route"""
    if request.method == 'GET':
        amenities = storage.all("Amenity").values()
        return jsonify(list(map(lambda x: x.to_dict(), amenities)))
    else:  # POST
        kwargs = request.get_json(force=True, silent=True)
        if kwargs is None:
            abort(400, "Not a JSON")
        if kwargs.get('name') is None:
            abort(400, "Missing name")
        amenity = Amenity(**kwargs)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<uuid:amenity_id>",
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id):
    """amenity route"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({})
    else:  # PUT
        kwargs = request.get_json(force=True, silent=True)
        if kwargs is None:
            abort(400, "Not a JSON")
        for key in kwargs:
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(amenity, key, kwargs.get(key))
        storage.save()
        return jsonify(amenity.to_dict())

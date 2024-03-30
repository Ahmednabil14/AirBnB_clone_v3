#!/usr/bin/python3
""" places """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<uuid:city_id>/places",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """places route"""
    city = storage.get(City, f'{city_id}')
    if city is None:
        abort(404)
    if request.method == 'GET':
        places = city.places
        return jsonify(list(map(lambda x: x.to_dict(), places)))
    else:  # POST
        kwargs = request.get_json(force=True, silent=True)
        if kwargs is None:
            abort(400, "Not a JSON")
        user_id = kwargs.get('user_id')
        if user_id is None:
            abort(400, "Missing user_id")
        if storage.get(User, user_id) is None:
            abort(404)
        if kwargs.get('name') is None:
            abort(400, "Missing name")
        place = Place(city_id=city_id, **kwargs)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<uuid:place_id>",
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """place route"""
    place = storage.get(Place, f'{place_id}')
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({})
    else:  # PUT
        kwargs = request.get_json(force=True, silent=True)
        if kwargs is None:
            abort(400, "Not a JSON")
        for key in kwargs:
            if key not in ('id', 'user_id', 'city_id',
                           'created_at', 'updated_at'):
                setattr(place, key, kwargs.get(key))
        storage.save()
        return jsonify(place.to_dict())

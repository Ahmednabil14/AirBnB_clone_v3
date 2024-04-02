#!/usr/bin/python3
""" places """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<uuid:city_id>/places",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """places route"""
    city = storage.get(City, city_id)
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
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<uuid:place_id>",
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """place route"""
    place = storage.get(Place, place_id)
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


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def places_search():
    """places_search route"""
    kwargs = request.get_json(force=True, silent=True)
    if kwargs is None:
        abort(400, "Not a JSON")
    state_ids = kwargs.get('states', [])
    city_ids = kwargs.get('cities', [])
    if state_ids == city_ids == []:
        places = storage.all('Place').values()
    else:
        cities = list(map(lambda id: storage.get(City, id), city_ids))
        for id in state_ids:
            cities += storage.get('State', id).cities
        cities = list(set(cities))
        places = []
        for city in cities:
            places += city.places
    amenities = kwargs.get('amenities', [])
    for place in places:
        if storage_t == 'db':
            if any(storage.get('Amenity', id) not in place.amenities
                   for id in amenities):
                places.remove(place)
        else:
            if any(amenity_id not in place.amenity_ids
                   for amenity_id in amenities):
                places.remove(place)
    places = list(map(lambda x: x.to_dict(), places))
    return jsonify(places)

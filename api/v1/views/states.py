#!/usr/bin/python3
""" states """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states",
                 methods=['GET', 'POST'],
                 strict_slashes=False)
def states():
    """states route"""
    if request.method == 'GET':
        states = storage.all("State").values()
        return jsonify(list(map(lambda x: x.to_dict(), states)))
    else:  # POST
        stated = request.get_json()
        if stated is None:
            return "Not a JSON", 400
        if stated.get('name') is None:
            return "Missing name", 400
        state = State(**stated)
        state.save()
        return state.to_dict(), 201


@app_views.route("/states/<uuid:state_id>",
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id):
    """state route"""
    state = storage.get(State, f'{state_id}')
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        state.delete()
        storage.save()
        return {}, 200
    else:  # PUT
        stated = request.get_json()
        if stated is None:
            return "Not a JSON", 400
        for key in stated:
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, stated.get(key))
        storage.save()
        return state.to_dict(), 200

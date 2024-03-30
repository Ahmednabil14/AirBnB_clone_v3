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
        kwargs = request.get_json()
        if kwargs is None:
            abort(400, "Not a JSON")
        if kwargs.get('name') is None:
            abort(400, "Missing name")
        state = State(**kwargs)
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
        kwargs = request.get_json()
        if kwargs is None:
            abort(400, "Not a JSON")
        for key in kwargs:
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, kwargs.get(key))
        storage.save()
        return state.to_dict(), 200

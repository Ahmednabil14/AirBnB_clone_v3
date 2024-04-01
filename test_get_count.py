#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.user import User


user1 = User(email="ahmed1@gmail.com", password="123", first_name="ahmed", last_name="ahmed")
user2 = User(email="ahmed1@gmail.com", password="123", first_name="ahmed", last_name="ahmed")
user3 = User(email="ahmed1@gmail.com", password="123", first_name="ahmed", last_name="ahmed")
user4 = User(email="ahmed1@gmail.com", password="123", first_name="ahmed", last_name="ahmed")

print(storage.all(User).values().id)

import json
import os

from django.contrib.auth.models import User


def create_superuser(username, password, email):
    User.objects.create_superuser(username=username, password=password, email=email)


def create_user(username, password, email):
    User.objects.create_user(username=username, password=password, email=email)


def enter_data(data):
    all_users = data['users']
    user = all_users['default']
    admin = all_users['admin']
    create_user(username=user['username'], password=user['password'], email=user['email'])
    create_superuser(username=admin['username'], password=admin['password'], email=admin['email'])

f = open(os.getcwd() + '/scripts/travis/variables.json', 'r')
data = json.load(f)
enter_data(data)
f.close()

import json
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from kitsune.settings import path


class Command(BaseCommand):
    help = 'Anonymize the database. Will wipe out some data.'

    def get_file_data(self):
        with open(path('scripts/travis/variables.json'), 'r') as f:
            data = json.load(f)
            return data

    def create_superuser(self, username, password, email):
        User.objects.create_superuser(username=username, password=password, email=email)

    def create_user(self, username, password, email):
        User.objects.create_user(username=username, password=password, email=email)

    def create_user_and_superuser(self, data):
        all_users = data['users']
        user = all_users['default']
        admin = all_users['admin']
        self.create_user(username=user['username'], password=user['password'], email=user['email'])
        self.create_superuser(username=admin['username'], password=admin['password'],
                              email=admin['email'])

    def handle(self, *arg, **kwargs):
        data = self.get_file_data()
        self.create_user_and_superuser(data)

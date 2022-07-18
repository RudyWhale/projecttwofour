from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from random import choices
import string
import argparse

from main.models import Guest


USER_HASH_LEN = 30


def add_guest(first_name: str, last_name: str):
    rnd_hash = ''.join(choices(string.ascii_uppercase + string.digits, k=USER_HASH_LEN))
    new_user = User.objects.create(first_name=first_name, last_name=last_name)
    new_guest = Guest.objects.create(user=new_user, hash=rnd_hash)
    new_user.save()
    new_guest.save()
    return rnd_hash


class Command(BaseCommand):
    help = 'Creates new guest with given first name and last name'

    def add_arguments(self, parser):
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)

    def handle(self, *args, **options):
        hash = add_guest(options['first_name'], options['last_name'])
        self.stdout.write(f'Created guest {options["first_name"]} {options["last_name"]} with hash {hash}')

from django.contrib.auth.models import User
from random import random
import string
import argparse

from ..models import Guest


def add_guest(first_name: str, last_name: str):
    rnd_hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
    new_user = User.objects.create(first_name=first_name, last_name=last_name)
    new_guest = Guest.objects.create(user=new_user, hash=rnd_hash)
    new_user.save()
    new_guest.save()
    return rnd_hash


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-fn', '--first_name', type=str)
    arg_parser.add_argument('-ln', '--last_name', type=str)
    args = arg_parser.parse_args()
    hash = add_guest(first_name=args.first_name, last_name=args.last_name)
    print(f'Created guest {args.first_name} {args.last_name} with hash {hash}')

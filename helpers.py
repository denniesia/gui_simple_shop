from canvas import frame
from hashlib import sha256
from json import loads, dump

def clean_screen():
    frame.delete('all')

def get_password_hash(password):
    hash_object = sha256(password.encode('UTF-8'))
    return hash_object.hexdigest()


def get_users_data():
    info_data = []

    with open("db/users_information.txt", "r") as users_file:
        for line in users_file:
            info_data.append(loads(line))

    return info_data


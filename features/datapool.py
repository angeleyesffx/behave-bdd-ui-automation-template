import os

DATA_ACCESS = {
    "python": {
        'language': 'python 3',
        'type': 0,
    },
    "ruby": {
        'language': 'ruby on rails',
        'type': 1,
    },
    "valid_user": {
        'email': os.environ.get('APP_USER'),
        'password': os.environ.get('APP_PASSWORD'),
    },
    "invalid_user": {
        'email': 'invalid.user@example.com',
        'password': 'WrongPassword',
    },
}

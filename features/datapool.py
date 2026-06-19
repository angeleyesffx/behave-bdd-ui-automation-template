import os

DATA_ACCESS = {
    "dress": {
        'keyword': 'dress',
        'type': 0,
    },
    "top": {
        'keyword': 'top',
        'type': 1,
    },
    "no_results": {
        'keyword': 'zzzznonexistent',
        'type': 2,
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

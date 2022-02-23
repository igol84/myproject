import requests

from prjstore.db.api import settings


class AuthException(Exception):  # Authexecption may be misspelled...
    pass


def auth(user_data):
    r = requests.post(f'{settings.host}/login',
                      data={'username': user_data['username'], 'password': user_data['password']})
    if r.status_code == 404:
        err = r.json()['detail']
        raise AuthException(err)
    elif r.status_code == 200:
        token = r.json()['access_token']
        store_id = r.json()['store_id']
        headers = {"Authorization": f"Bearer {token}", 'store_id': store_id}
        return headers
    else:
        raise ConnectionError

import requests

from prjstore.db.api import settings


def auth():
    r = requests.post(f'{settings.host}/login', data={'username': settings.username, 'password': settings.password})
    if r.status_code == 404:
        err = r.json()['detail']
        raise ValueError(err)
    elif r.status_code == 200:
        token = r.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        return headers
    else:
        raise ConnectionError

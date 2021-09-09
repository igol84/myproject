import requests

host = 'http://31.148.245.50'
username = 'qwe'
password = 'qwe'

r = requests.post(f'{host}/login', data={'username':username, 'password':password})
token = r.json()['access_token']
headers = {"Authorization": f"Bearer {token}"}
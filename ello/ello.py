import json
import requests
from urllib.parse import urljoin


class Ello:
    api_base_url = 'https://ello.co/api/v2/'
    webapp_token_url = 'https://ello.co/api/webapp-token'
    oauth_token_url = 'https://ello.co/api/oauth/token'
    default_client_id = (
        'd5cb8b75cb11fa3304fd973a8daa0b3601042d13f8e255971caecde3d2396e3d'
    )

    def _get_headers(self):
        headers = {
            'content-type': 'application/json',
            'authorization': ' '.join(['Bearer', self.token['access_token']])
        }
        return headers

    def _get_url(self, *args):
        return urljoin(self.api_base_url, '/'.join(args))

    def __init__(self, email, password, client_id=None):
        self.email = email
        self.password = password
        self.client_id = client_id or self.default_client_id

    def auth(self):
        response = requests.get(self.webapp_token_url)
        response.raise_for_status()
        token = response.json()['token']
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer {}'.format(token['access_token'])
        }
        payload = {
            "email": self.email,
            "password": self.password,
            "grant_type": "password",
            "client_id": self.client_id
        }
        response = requests.post(
            self.oauth_token_url,
            data=json.dumps(payload),
            headers=headers
        )
        response.raise_for_status()
        self.token = response.json()

    def profile(self):
        response = requests.get(
            self._get_url('profile'),
            params={'meta': 'true'},
            headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def categories(self):
        response = requests.get(
            self._get_url('categories'),
            params={'meta': 'true'},
            headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def recent_posts(self, category):
        response = requests.get(
            self._get_url('categories', category, 'posts', 'recent'),
            headers=self._get_headers())
        response.raise_for_status()
        return response.json()

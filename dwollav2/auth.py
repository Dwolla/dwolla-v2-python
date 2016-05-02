try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from dwollav2.error import Error


def auth_for(_client):
    class Auth:
        def __init__(self, **kwargs):
            self.redirect_uri = kwargs.get('redirect_uri')
            self.scope = kwargs.get('scope')
            self.state = kwargs.get('state')

        def url(self):
            return '%s?%s' % (_client.auth_url(), urlencode(self._query()))

        def callback(self, params):
            if params.get('state') != self.state:
                raise ValueError('invalid state')
            if 'error' in params:
                raise Error.map(params)
            payload = {
                'client_id': _client.id,
                'client_secret': _client.secret,
                'grant_type': 'authorization_code',
                'code': params['code'],
                'redirect_uri': self.redirect_uri
            }
            res = requests.post(_client.token_url(), data=payload)
            if Auth.is_error(res):
                raise Error.map(res)
            token = _client.Token(res.json())
            if _client.on_grant is not None:
                _client.on_grant(token)
            return token

        def _query(self):
            d = {
                'response_type': 'code',
                'client_id': _client.id,
                'redirect_uri': self.redirect_uri,
                'scope': self.scope,
                'state': self.state
            }
            return dict((k, v) for k, v in iter(d.items()) if v)

        @staticmethod
        def client():
            payload = {
                'client_id': _client.id,
                'client_secret': _client.secret,
                'grant_type': 'client_credentials'
            }
            res = requests.post(_client.token_url(), data=payload)
            if Auth.is_error(res):
                raise Error.map(res)
            token = _client.Token(res.json())
            if _client.on_grant is not None:
                _client.on_grant(token)
            return token

        @staticmethod
        def is_error(res):
            try:
                return 'error' in res.json()
            except:
                return True

    return Auth

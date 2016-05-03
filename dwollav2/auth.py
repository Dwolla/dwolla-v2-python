try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from dwollav2.error import Error
from dwollav2.version import version


def _is_error(res):
    try:
        return 'error' in res.json()
    except:
        return True

def _request_token(client, payload):
    headers = {
        'user-agent': 'dwolla-v2-python %s' % version
    }
    res = requests.post(client.token_url, data=payload, headers=headers)
    if _is_error(res):
        raise Error.map(res)
    token = client.Token(res.json())
    if client.on_grant is not None:
        client.on_grant(token)
    return token

def auth_for(_client):
    class Auth:
        def __init__(self, **kwargs):
            self.redirect_uri = kwargs.get('redirect_uri')
            self.scope = kwargs.get('scope')
            self.state = kwargs.get('state')

        @property
        def url(self):
            return '%s?%s' % (_client.auth_url, urlencode(self._query()))

        def callback(self, params):
            if params.get('state') != self.state:
                raise ValueError('invalid state')
            if 'error' in params:
                raise Error.map(params)
            return _request_token(_client, {
                'client_id': _client.id,
                'client_secret': _client.secret,
                'grant_type': 'authorization_code',
                'code': params['code'],
                'redirect_uri': self.redirect_uri
            })

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
            return _request_token(_client, {
                'client_id': _client.id,
                'client_secret': _client.secret,
                'grant_type': 'client_credentials'
            })

        @staticmethod
        def refresh(token):
            return _request_token(_client, {
                'client_id': _client.id,
                'client_secret': _client.secret,
                'grant_type': 'refresh_token',
                'refresh_token': token.refresh_token
            })

    return Auth

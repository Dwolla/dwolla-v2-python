from dwollav2.auth import auth_for
from dwollav2.token import token_for


class Client:
    ENVIRONMENTS = {
        'production': {
            'auth_url':  'https://accounts.dwolla.com/auth',
            'token_url': 'https://api.dwolla.com/token',
            'api_url':   'https://api.dwolla.com'
        },
        'sandbox': {
            'auth_url':  'https://accounts-sandbox.dwolla.com/auth',
            'token_url': 'https://api-sandbox.dwolla.com/token',
            'api_url':   'https://api-sandbox.dwolla.com'
        }
    }

    def __init__(self, **kwargs):
        self.id = self.key = kwargs.get('id') or kwargs['key']
        self.secret = kwargs['secret']
        self.environment = kwargs.get('environment', 'production')
        if self.environment not in self.ENVIRONMENTS:
            raise ValueError('invalid environment')
        self.on_grant = kwargs.get('on_grant')
        self.Auth = auth_for(self)
        self.Token = token_for(self)

    def auth(self, opts=None, **kwargs):
        return self.Auth(opts, **kwargs)

    def refresh_token(self, opts=None, **kwargs):
        return self.Auth.refresh(self.Token(opts, **kwargs))

    def token(self, opts=None, **kwargs):
        return self.Token(opts, **kwargs)

    @property
    def auth_url(self):
        return self.ENVIRONMENTS[self.environment]['auth_url']

    @property
    def token_url(self):
        return self.ENVIRONMENTS[self.environment]['token_url']

    @property
    def api_url(self):
        return self.ENVIRONMENTS[self.environment]['api_url']

    def Token(self, opts=None, **kwargs):
        return Token(self, opts, **kwargs)

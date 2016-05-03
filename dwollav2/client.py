from dwollav2.auth import auth_for
from dwollav2.token import token_for


class Client:
    ENVIRONMENTS = {
      'production': {
        'auth_url':  'https://www.dwolla.com/oauth/v2/authenticate',
        'token_url': 'https://www.dwolla.com/oauth/v2/token',
        'api_url':   'https://api.dwolla.com'
      },
      'sandbox': {
        'auth_url':  'https://uat.dwolla.com/oauth/v2/authenticate',
        'token_url': 'https://uat.dwolla.com/oauth/v2/token',
        'api_url':   'https://api-uat.dwolla.com'
      }
    }

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.secret = kwargs['secret']
        self.environment = kwargs.get('environment', 'production')
        if self.environment not in self.ENVIRONMENTS:
            raise ValueError('invalid environment')
        self.on_grant = kwargs.get('on_grant')
        self.Auth = auth_for(self)
        self.Token = token_for(self)

    @property
    def auth_url(self):
        return self.ENVIRONMENTS[self.environment]['auth_url']

    @property
    def token_url(self):
        return self.ENVIRONMENTS[self.environment]['token_url']

    @property
    def api_url(self):
        return self.ENVIRONMENTS[self.environment]['api_url']

    def Token(self, opts = None, **kwargs):
        return Token(self, opts, **kwargs)

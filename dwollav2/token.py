import requests
from io import IOBase
import re

from dwollav2.response import Response
from dwollav2.version import version


def _items_or_iteritems(o):
    try:
        return o.iteritems()
    except:
        return o.items()


def _is_a_file(o):
    try:
        return isinstance(o, file) or isinstance(o, IOBase)
    except NameError as e:
        return isinstance(o, IOBase)


def _contains_file(o):
    if isinstance(o, dict):
        for k, v in _items_or_iteritems(o):
            if _contains_file(v):
                return True
        return False
    elif isinstance(o, tuple) or isinstance(o, list):
        for v in o:
            if _contains_file(v):
                return True
        return False
    else:
        return _is_a_file(o)


def token_for(_client):
    class Token:
        def __init__(self, opts=None, **kwargs):
            opts = kwargs if opts is None else opts
            self.access_token = opts.get('access_token')
            self.refresh_token = opts.get('refresh_token')
            self.expires_in = opts.get('expires_in')
            self.scope = opts.get('scope')
            self.app_id = opts.get('app_id')
            self.account_id = opts.get('account_id')

            self.session = requests.session()
            self.session.headers.update({
                'accept': 'application/vnd.dwolla.v1.hal+json',
                'user-agent': 'dwolla-v2-python %s' % version,
                'authorization': 'Bearer %s' % self.access_token
            })

        def post(self, url, body=None, headers={}, **kwargs):
            body = kwargs if body is None else body
            if _contains_file(body):
                files = [(k, v) for k, v in _items_or_iteritems(
                    body) if _contains_file(v)]
                data = [(k, v) for k, v in _items_or_iteritems(
                    body) if not _contains_file(v)]
                return Response(self.session.post(self._full_url(url), headers=headers, files=files, data=data, **kwargs))
            else:
                return Response(self.session.post(self._full_url(url), headers=headers, json=body, **kwargs))

        def get(self, url, params=None, headers={}, **kwargs):
            params = kwargs if params is None else params
            return Response(self.session.get(self._full_url(url), headers=headers, params=params, **kwargs))

        def delete(self, url, params=None, headers={}, **kwargs):
            return Response(self.session.delete(self._full_url(url), headers=headers, params=params, **kwargs))

        def _full_url(self, path):
            if isinstance(path, dict):
                path = path['_links']['self']['href']

            if path.startswith(_client.api_url):
                return path
            elif path.startswith('/'):
                return _client.api_url + path
            else:
                path = re.sub(r'^https?://[^/]*/', '', path)
                return "%s/%s" % (_client.api_url, path)

    return Token

import requests
from io import IOBase
import re

try:
    import simplejson as json
except ImportError:
    import json

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

            self._session = requests.session()
            self._session.headers.update({
                'accept': 'application/vnd.dwolla.v1.hal+json',
                'user-agent': 'dwolla-v2-python %s' % version,
                'authorization': 'Bearer %s' % self.access_token
            })

        def post(self, url, body=None, headers={}, **kwargs):
            body = kwargs if body is None else body
            requests = _client.requests.copy()
            headers = self._merge_dicts(
                requests.pop('headers', {}), headers)
            if _contains_file(body):
                files = [(k, v) for k, v in _items_or_iteritems(
                    body) if _contains_file(v)]
                data = [(k, v) for k, v in _items_or_iteritems(
                    body) if not _contains_file(v)]
                return Response(self._session.post(self._full_url(url), headers=headers, files=files, data=data, **requests))
            else:
                return Response(self._session.post(
                    self._full_url(url),
                    headers=self._merge_dicts(
                        {'content-type': 'application/json'}, headers),
                    data=json.dumps(body, sort_keys=True, indent=2),
                    **requests))

        def get(self, url, params=None, headers={}, **kwargs):
            params = kwargs if params is None else params
            requests = _client.requests.copy()
            headers = self._merge_dicts(
                requests.pop('headers', {}), headers)
            return Response(self._session.get(self._full_url(url), headers=headers, params=params, **requests))

        def delete(self, url, params=None, headers={}):
            requests = _client.requests.copy()
            headers = self._merge_dicts(
                requests.pop('headers', {}), headers)
            return Response(self._session.delete(self._full_url(url), headers=headers, params=params, **requests))

        def _full_url(self, path):
            if isinstance(path, dict):
                path = path['_links']['self']['href']
            if path.startswith(_client.api_url) and _client.api_url[-1] == '/':
                return path
            elif path.startswith('/'):
                return _client.api_url + path
            else:
                path = re.sub(r'^https?://[^/]*/', '', path)
                return "%s/%s" % (_client.api_url, path)

        def _merge_dicts(self, x, y):
            z = x.copy()   # start with x's keys and values
            z.update(y)    # modifies z with y's keys and values & returns None
            return z

    return Token

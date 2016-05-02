import requests

from dwollav2.response import Response


def _contains_file(o):
    if isinstance(o, dict):
        for k, v in o.iteritems():
            if _contains_file(v):
                return True
        return False
    elif isinstance(o, tuple) or isinstance(o, list):
        for v in o:
            if _contains_file(v):
                return True
        return False
    else:
        return isinstance(o, file)

def token_for(_client):
    class Token:
        def __init__(self, opts = None, **kwargs):
            args = kwargs if opts is None else opts
            self.access_token  = args.get('access_token')
            self.refresh_token = args.get('refresh_token')
            self.expires_in    = args.get('expires_in')
            self.scope         = args.get('scope')
            self.app_id        = args.get('app_id')
            self.account_id    = args.get('account_id')

        def post(self, url, body={}):
            if _contains_file(body):
                files = [(k, v) for k, v in body.iteritems() if _contains_file(v)]
                data = [(k, v) for k, v in body.iteritems() if not _contains_file(v)]
                return Response(requests.post(self._full_url(url), headers=self._headers(), files=files, data=data))
            else:
                return Response(requests.post(self._full_url(url), headers=self._headers(), json=body))

        def get(self, url, params={}):
            return Response(requests.get(self._full_url(url), headers=self._headers(), params=params))

        def delete(self, url):
            return Response(requests.delete(self._full_url(url), headers=self._headers()))

        def _headers(self):
            return {
                'accept': 'application/vnd.dwolla.v1.hal+json',
                'authorization': 'Bearer %s' % self.access_token
            }

        def _full_url(self, path):
            if isinstance(path, dict):
                path = path['_links']['self']['href']

            if path.startswith(_client.api_url()):
                return path
            elif path.startswith('/'):
                return _client.api_url() + path
            else:
                return "%s/%s" % (_client.api_url(), path)

    return Token

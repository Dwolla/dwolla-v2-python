import unittest2
import responses

import dwollav2


class TokenShould(unittest2.TestCase):
    client = dwollav2.Client(id='id', secret='secret')
    access_token = 'access token'
    refresh_token = 'refresh token'
    expires_in = 123
    scope = 'scope'
    account_id = 'account id'

    def test_sets_access_token(self):
        token = self.client.Token(access_token=self.access_token)
        self.assertEqual(self.access_token, token.access_token)

    def test_sets_refresh_token(self):
        token = self.client.Token(refresh_token=self.refresh_token)
        self.assertEqual(self.refresh_token, token.refresh_token)

    def test_sets_expires_in(self):
        token = self.client.Token(expires_in=self.expires_in)
        self.assertEqual(self.expires_in, token.expires_in)

    def test_sets_scope(self):
        token = self.client.Token(scope=self.scope)
        self.assertEqual(self.scope, token.scope)

    def test_sets_account_id(self):
        token = self.client.Token(account_id=self.account_id)
        self.assertEqual(self.account_id, token.account_id)

    @responses.activate
    def test_get_success(self):
        responses.add(responses.GET,
                      self.client.api_url() + '/foo',
                      body='{"foo": "bar"}',
                      status=200,
                      content_type='application/vnd.dwolla.v1.hal+json')
        token = self.client.Token(access_token=self.access_token)
        res = token.get('foo')
        self.assertEqual(200, res.status)
        self.assertEqual({'foo': 'bar'}, res.body)

    @responses.activate
    def test_get_success_leading_slash(self):
        responses.add(responses.GET,
                      self.client.api_url() + '/foo',
                      body='{"foo": "bar"}',
                      status=200,
                      content_type='application/vnd.dwolla.v1.hal+json')
        token = self.client.Token(access_token=self.access_token)
        res = token.get('/foo')
        self.assertEqual(200, res.status)
        self.assertEqual({'foo': 'bar'}, res.body)

    @responses.activate
    def test_get_success_full_url(self):
        responses.add(responses.GET,
                      self.client.api_url() + '/foo',
                      body='{"foo": "bar"}',
                      status=200,
                      content_type='application/vnd.dwolla.v1.hal+json')
        token = self.client.Token(access_token=self.access_token)
        res = token.get(self.client.api_url() + '/foo')
        self.assertEqual(200, res.status)
        self.assertEqual({'foo': 'bar'}, res.body)

    @responses.activate
    def test_get_error(self):
        responses.add(responses.GET,
                      self.client.api_url() + '/foo',
                      body='{"error": "bad"}',
                      status=400,
                      content_type='application/vnd.dwolla.v1.hal+json')
        token = self.client.Token(access_token=self.access_token)
        with self.assertRaises(dwollav2.Error):
            token.get('foo')

    @responses.activate
    def test_post_success(self):
        responses.add(responses.POST,
                      self.client.api_url() + '/foo',
                      body='{"foo": "bar"}',
                      status=200,
                      content_type='application/vnd.dwolla.v1.hal+json')
        token = self.client.Token(access_token=self.access_token)
        res = token.post('foo')
        self.assertEqual(200, res.status)
        self.assertEqual({'foo': 'bar'}, res.body)

    @responses.activate
    def test_delete_success(self):
        responses.add(responses.DELETE,
                      self.client.api_url() + '/foo',
                      body='{"foo": "bar"}',
                      status=200,
                      content_type='application/vnd.dwolla.v1.hal+json')
        token = self.client.Token(access_token=self.access_token)
        res = token.delete('foo')
        self.assertEqual(200, res.status)
        self.assertEqual({'foo': 'bar'}, res.body)

import unittest2
import responses
from mock import Mock
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import dwollav2


class AuthShould(unittest2.TestCase):
    client = dwollav2.Client(id='id', secret='secret', on_grant=Mock())
    redirect_uri = 'redirect uri'
    scope = 'scope'
    state = 'state'

    def test_instance_sets_redirect_uri(self):
        auth = self.client.Auth(redirect_uri = self.redirect_uri)
        self.assertEqual(self.redirect_uri, auth.redirect_uri)

    def test_instance_sets_scope(self):
        auth = self.client.Auth(scope = self.scope)
        self.assertEqual(self.scope, auth.scope)

    def test_instance_sets_state(self):
        auth = self.client.Auth(state = self.state)
        self.assertEqual(self.state, auth.state)

    def test_instance_url(self):
        auth = self.client.Auth(redirect_uri = self.redirect_uri,
                                scope = self.scope,
                                state = self.state)
        expected_url = '%s' % self.client.auth_url
        self.assertEqual(expected_url, auth.url)

    def test_instance_url(self):
        auth = self.client.Auth(redirect_uri = self.redirect_uri,
                                scope = self.scope,
                                state = self.state)
        expected_url = self.client.auth_url + '?' + self._expected_query(self.client, auth)
        self.assertEqual(expected_url, auth.url)

    def test_instance_callback_raises_error_if_state_mismatch(self):
        auth = self.client.Auth(redirect_uri = self.redirect_uri,
                                scope = self.scope,
                                state = self.state)
        params = {'state': self.state + 'bad'}
        with self.assertRaises(ValueError):
            auth.callback(params)

    def test_instance_callback_raises_error_if_passed_error(self):
        auth = self.client.Auth(redirect_uri = self.redirect_uri,
                                scope = self.scope,
                                state = self.state)
        params = {'error': 'bad', 'state': self.state}
        with self.assertRaises(dwollav2.Error):
            auth.callback(params)

    @responses.activate
    def test_instance_callback_success(self):
        auth = self.client.Auth(redirect_uri = self.redirect_uri,
                                scope = self.scope,
                                state = self.state)
        responses.add(responses.POST,
                      self.client.token_url,
                      body='{"access_token": "abc"}',
                      status=200,
                      content_type='application/json')
        params = {'state': self.state, 'code': 'def'}
        token = auth.callback(params)
        self.assertEqual('abc', token.access_token)
        self.client.on_grant.assert_called_with(token)

    @responses.activate
    def test_instance_callback_error(self):
        auth = self.client.Auth(redirect_uri = self.redirect_uri,
                                scope = self.scope,
                                state = self.state)
        responses.add(responses.POST,
                      self.client.token_url,
                      body='{"error": "bad"}',
                      status=200,
                      content_type='application/json')
        params = {'state': self.state, 'code': 'def'}
        with self.assertRaises(dwollav2.Error):
            auth.callback(params)

    @responses.activate
    def test_instance_callback_success_with_none_on_grant(self):
        client = dwollav2.Client(id='id', secret='secret')
        auth = client.Auth(redirect_uri = self.redirect_uri,
                           scope = self.scope,
                           state = self.state)
        responses.add(responses.POST,
                      client.token_url,
                      body='{"access_token": "abc"}',
                      status=200,
                      content_type='application/json')
        params = {'state': self.state, 'code': 'def'}
        token = auth.callback(params)
        self.assertEqual('abc', token.access_token)

    @responses.activate
    def test_class_client_success(self):
        responses.add(responses.POST,
                      self.client.token_url,
                      body='{"access_token": "abc"}',
                      status=200,
                      content_type='application/json')
        token = self.client.Auth.client()
        self.assertEqual('abc', token.access_token)
        self.client.on_grant.assert_called_with(token)

    @responses.activate
    def test_class_client_error(self):
        responses.add(responses.POST,
                      self.client.token_url,
                      body='{"error": "bad"}',
                      status=200,
                      content_type='application/json')
        with self.assertRaises(dwollav2.Error):
            self.client.Auth.client()

    @responses.activate
    def test_class_refresh_success(self):
        responses.add(responses.POST,
                      self.client.token_url,
                      body='{"access_token": "abc"}',
                      status=200,
                      content_type='application/json')
        old_token = self.client.Token(refresh_token = 'refresh token')
        token = self.client.Auth.refresh(old_token)
        self.assertEqual('abc', token.access_token)
        self.client.on_grant.assert_called_with(token)

    @responses.activate
    def test_class_refresh_error(self):
        responses.add(responses.POST,
                      self.client.token_url,
                      body='{"error": "bad"}',
                      status=200,
                      content_type='application/json')
        old_token = self.client.Token(refresh_token = 'refresh token')
        with self.assertRaises(dwollav2.Error):
            self.client.Auth.refresh(old_token)

    def _expected_query(self, client, auth):
        d = {
            'response_type': 'code',
            'client_id': client.id,
            'redirect_uri': auth.redirect_uri,
            'scope': auth.scope,
            'state': auth.state,
            'verified_account': auth.verified_account,
            'dwolla_landing': auth.dwolla_landing
        }
        return urlencode(dict((k, v) for k, v in iter(d.items()) if v))

import unittest
import responses

import dwollav2


class ClientShould(unittest.TestCase):
    id = 'client-id'
    secret = 'client-secret'

    def test_sets_id_and_key_when_id_provided(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        self.assertEqual(self.id, client.id)
        self.assertEqual(self.id, client.key)

    def test_sets_id_and_key_when_key_provided(self):
        client = dwollav2.Client(key=self.id, secret=self.secret)
        self.assertEqual(self.id, client.id)
        self.assertEqual(self.id, client.key)

    def test_sets_secret(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        self.assertEqual(self.secret, client.secret)

    def test_sets_environment(self):
        client = dwollav2.Client(
            id=self.id, secret=self.secret, environment='sandbox')
        self.assertEqual('sandbox', client.environment)

    def test_raises_if_invalid_environment(self):
        with self.assertRaises(ValueError):
            dwollav2.Client(id=self.id, secret=self.secret,
                            environment='invalid')

    def test_sets_on_grant(self):
        def on_grant(x): return x
        client = dwollav2.Client(
            id=self.id, secret=self.secret, on_grant=on_grant)
        self.assertEqual(on_grant, client.on_grant)

    def test_auth_url(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        self.assertEqual(
            client.ENVIRONMENTS[client.environment]['auth_url'], client.auth_url)

    def test_token_url(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        self.assertEqual(
            client.ENVIRONMENTS[client.environment]['token_url'], client.token_url)

    def test_api_url(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        self.assertEqual(
            client.ENVIRONMENTS[client.environment]['api_url'], client.api_url)

    def test_auth(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        redirect_uri = "redirect-uri"
        self.assertEqual(client.auth(
            redirect_uri=redirect_uri).url, 'https://accounts.dwolla.com/auth?client_id=client-id&redirect_uri=%s&response_type=code' % redirect_uri)

    @responses.activate
    def test_refresh_token_success(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        responses.add(responses.POST,
                      client.token_url,
                      body='{"access_token": "abc"}',
                      status=200,
                      content_type='application/json')
        token = client.refresh_token(refresh_token='refresh-token')
        self.assertEqual('abc', token.access_token)

    @responses.activate
    def test_refresh_token_error(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        responses.add(responses.POST,
                      client.token_url,
                      body='{"error": "bad"}',
                      status=200,
                      content_type='application/json')
        with self.assertRaises(dwollav2.Error):
            client.refresh_token(refresh_token='refresh-token')

    def test_token(self):
        client = dwollav2.Client(id=self.id, secret=self.secret)
        access_token = "access-token"
        self.assertEqual(client.token(
            access_token=access_token).access_token, access_token)

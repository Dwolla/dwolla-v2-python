import unittest2

import dwollav2


class ClientShould(unittest2.TestCase):
    id = 'client-id'
    secret = 'client-secret'

    def test_sets_id_and_key_when_id_provided(self):
        client = dwollav2.Client(id = self.id, secret = self.secret)
        self.assertEqual(self.id, client.id)
        self.assertEqual(self.id, client.key)

    def test_sets_id_and_key_when_key_provided(self):
        client = dwollav2.Client(key = self.id, secret = self.secret)
        self.assertEqual(self.id, client.id)
        self.assertEqual(self.id, client.key)

    def test_sets_secret(self):
        client = dwollav2.Client(id = self.id, secret = self.secret)
        self.assertEqual(self.secret, client.secret)

    def test_sets_environment(self):
        client = dwollav2.Client(id = self.id, secret = self.secret, environment = 'sandbox')
        self.assertEqual('sandbox', client.environment)

    def test_raises_if_invalid_environment(self):
        with self.assertRaises(ValueError):
            dwollav2.Client(id = self.id, secret = self.secret, environment = 'invalid')

    def test_sets_on_grant(self):
        on_grant = lambda x: x
        client = dwollav2.Client(id = self.id, secret = self.secret, on_grant = on_grant)
        self.assertEqual(on_grant, client.on_grant)

    def test_auth_url(self):
        client = dwollav2.Client(id = self.id, secret = self.secret)
        self.assertEqual(client.ENVIRONMENTS[client.environment]['auth_url'], client.auth_url)

    def test_token_url(self):
        client = dwollav2.Client(id = self.id, secret = self.secret)
        self.assertEqual(client.ENVIRONMENTS[client.environment]['token_url'], client.token_url)

    def test_api_url(self):
        client = dwollav2.Client(id = self.id, secret = self.secret)
        self.assertEqual(client.ENVIRONMENTS[client.environment]['api_url'], client.api_url)

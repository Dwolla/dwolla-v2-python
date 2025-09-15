import unittest
import requests

import dwollav2


class ResponseShould(unittest.TestCase):
    def test_raises_error_if_over_400(self):
        res = requests.Response()
        res.status_code = 400
        with self.assertRaises(dwollav2.Error):
            dwollav2.Response(res)

    def test_sets_status(self):
        res = requests.Response()
        res.status_code = 200
        dres = dwollav2.Response(res)
        self.assertEqual(res.status_code, dres.status)

    def test_sets_headers(self):
        res = requests.Response()
        res.status_code = 200
        res.headers = {'foo': 'bar'}
        dres = dwollav2.Response(res)
        self.assertEqual(res.headers, dres.headers)

    def test_sets_text_body(self):
        res = requests.Response()
        res.status_code = 200
        res._content = 'foo bar'.encode()
        dres = dwollav2.Response(res)
        self.assertEqual(res.text, dres.body)

    def test_sets_json_body(self):
        res = requests.Response()
        res.status_code = 200
        res._content = '{"foo":"bar"}'.encode()
        dres = dwollav2.Response(res)
        self.assertEqual(res.json(), dres.body)

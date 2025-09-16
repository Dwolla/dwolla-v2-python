import unittest
import requests

import dwollav2


class ErrorShould(unittest.TestCase):
    def test_maps_string_to_generic_error(self):
        error = 'foo'
        with self.assertRaises(dwollav2.Error) as ecm:
            raise dwollav2.Error.map(error)
        self.assertEqual(error, str(ecm.exception))
        self.assertEqual(error, ecm.exception.body)

    def test_maps_dict_to_specific_error(self):
        error = {'error': 'invalid_request'}
        with self.assertRaises(dwollav2.InvalidRequestError) as ecm:
            raise dwollav2.Error.map(error)
        self.assertEqual(str(error), str(ecm.exception))
        self.assertEqual(error, ecm.exception.body)

    def test_maps_response(self):
        res = requests.Response()
        res.status_code = 420
        res.headers = {'foo': 'bar'}
        res._content = '{"error":"invalid_request"}'.encode()
        with self.assertRaises(dwollav2.InvalidRequestError) as ecm:
            raise dwollav2.Error.map(res)
        self.assertEqual(res.text, str(ecm.exception))
        self.assertEqual(res.status_code, ecm.exception.status)
        self.assertEqual(res.headers, ecm.exception.headers)
        self.assertEqual(res.json(), ecm.exception.body)

    def test_maps_codes(self):
        self._test_maps_code_to_error('access_denied', dwollav2.AccessDeniedError)
        self._test_maps_code_to_error('InvalidCredentials', dwollav2.InvalidCredentialsError)
        self._test_maps_code_to_error('NotFound', dwollav2.NotFoundError)
        self._test_maps_code_to_error('BadRequest', dwollav2.BadRequestError)
        self._test_maps_code_to_error('invalid_grant', dwollav2.InvalidGrantError)
        self._test_maps_code_to_error('RequestTimeout', dwollav2.RequestTimeoutError)
        self._test_maps_code_to_error('ExpiredAccessToken', dwollav2.ExpiredAccessTokenError)
        self._test_maps_code_to_error('invalid_request', dwollav2.InvalidRequestError)
        self._test_maps_code_to_error('ServerError', dwollav2.ServerError)
        self._test_maps_code_to_error('Forbidden', dwollav2.ForbiddenError)
        self._test_maps_code_to_error('InvalidResourceState', dwollav2.InvalidResourceStateError)
        self._test_maps_code_to_error('temporarily_unavailable', dwollav2.TemporarilyUnavailableError)
        self._test_maps_code_to_error('InvalidAccessToken', dwollav2.InvalidAccessTokenError)
        self._test_maps_code_to_error('InvalidScope', dwollav2.InvalidScopeError)
        self._test_maps_code_to_error('unauthorized_client', dwollav2.UnauthorizedClientError)
        self._test_maps_code_to_error('InvalidAccountStatus', dwollav2.InvalidAccountStatusError)
        self._test_maps_code_to_error('unsupported_grant_type', dwollav2.UnsupportedGrantTypeError)
        self._test_maps_code_to_error('InvalidApplicationStatus', dwollav2.InvalidApplicationStatusError)
        self._test_maps_code_to_error('InvalidVersion', dwollav2.InvalidVersionError)
        self._test_maps_code_to_error('unsupported_response_type', dwollav2.UnsupportedResponseTypeError)
        self._test_maps_code_to_error('invalid_client', dwollav2.InvalidClientError)
        self._test_maps_code_to_error('method_not_allowed', dwollav2.MethodNotAllowedError)
        self._test_maps_code_to_error('ValidationError', dwollav2.ValidationError)
        self._test_maps_code_to_error('TooManyRequests', dwollav2.TooManyRequestsError)
        self._test_maps_code_to_error('Conflict', dwollav2.ConflictError)
        self._test_maps_code_to_error('UpdateCredentials', dwollav2.UpdateCredentialsError)

    def _test_maps_code_to_error(self, code, klass):
        error = {'error': code}
        error2 = {'code': code}
        with self.assertRaises(klass):
            raise dwollav2.Error.map(error)
        with self.assertRaises(klass):
            raise dwollav2.Error.map(error2)

import requests

class Error(Exception):
    def __init__(self, res):
        if isinstance(res, requests.Response):
            super(Error, self).__init__(res.text)
            self.status = res.status_code
            self.headers = res.headers
            self.body = self._get_body(res)
        else:
            super(Error, self).__init__(str(res))
            self.body = res

    @staticmethod
    def map(res):
        try:
            if isinstance(res, requests.Response):
                body = res.json()
            else:
                body = res
            c = body.get('code', body.get('error'))
        except:
            c = None

        return {
            'access_denied':             AccessDeniedError,
            'InvalidCredentials':        InvalidCredentialsError,
            'NotFound':                  NotFoundError,
            'BadRequest':                BadRequestError,
            'invalid_grant':             InvalidGrantError,
            'RequestTimeout':            RequestTimeoutError,
            'ExpiredAccessToken':        ExpiredAccessTokenError,
            'invalid_request':           InvalidRequestError,
            'ServerError':               ServerError,
            'Forbidden':                 ForbiddenError,
            'InvalidResourceState':      InvalidResourceStateError,
            'temporarily_unavailable':   TemporarilyUnavailableError,
            'InvalidAccessToken':        InvalidAccessTokenError,
            'InvalidScope':              InvalidScopeError,
            'unauthorized_client':       UnauthorizedClientError,
            'InvalidAccountStatus':      InvalidAccountStatusError,
            'unsupported_grant_type':    UnsupportedGrantTypeError,
            'InvalidApplicationStatus':  InvalidApplicationStatusError,
            'InvalidVersion':            InvalidVersionError,
            'unsupported_response_type': UnsupportedResponseTypeError,
            'invalid_client':            InvalidClientError,
            'method_not_allowed':        MethodNotAllowedError,
            'ValidationError':           ValidationError,
            'TooManyRequests':           TooManyRequestsError,
            'Conflict':                  ConflictError
        }.get(c, Error)(res)

    def _get_body(self, res):
        try:
            return res.json()
        except:
            return res.text

class AccessDeniedError(Error):
    pass

class InvalidCredentialsError(Error):
    pass

class NotFoundError(Error):
    pass

class BadRequestError(Error):
    pass

class InvalidGrantError(Error):
    pass

class RequestTimeoutError(Error):
    pass

class ExpiredAccessTokenError(Error):
    pass

class InvalidRequestError(Error):
    pass

class ServerError(Error):
    pass

class ForbiddenError(Error):
    pass

class InvalidResourceStateError(Error):
    pass

class TemporarilyUnavailableError(Error):
    pass

class InvalidAccessTokenError(Error):
    pass

class InvalidScopeError(Error):
    pass

class UnauthorizedClientError(Error):
    pass

class InvalidAccountStatusError(Error):
    pass

class UnsupportedGrantTypeError(Error):
    pass

class InvalidApplicationStatusError(Error):
    pass

class InvalidVersionError(Error):
    pass

class UnsupportedResponseTypeError(Error):
    pass

class InvalidClientError(Error):
    pass

class MethodNotAllowedError(Error):
    pass

class ValidationError(Error):
    pass

class TooManyRequestsError(Error):
    pass

class ConflictError(Error):
    pass

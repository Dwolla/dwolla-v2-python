from dwollav2.error import Error


class Response:
    def __init__(self, res):
        if (res.status_code >= 400):
            raise Error.map(res)

        self.status = res.status_code
        self.headers = res.headers
        self.body = self._get_body(res)

    def _get_body(self, res):
        try:
            return res.json()
        except:
            return res.text

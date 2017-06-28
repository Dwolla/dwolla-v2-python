# DwollaV2

![Build Status](https://travis-ci.org/Dwolla/dwolla-v2-python.svg)

Dwolla V2 Python client. For the V1 Python client see [Dwolla/dwolla-python](https://github.com/Dwolla/dwolla-python).

[API Documentation](https://docsv2.dwolla.com)

## Installation

```
pip install dwollav2
```

## `dwollav2.Client`

### Basic usage

Create a client using your application's consumer key and secret found on the applications page
([Sandbox][apsandbox], [Production][approd]).

[apsandbox]: https://sandbox.dwolla.com/applications
[approd]: https://www.dwolla.com/applications

```python
client = dwollav2.Client(id = os.environ['DWOLLA_APP_KEY'], secret = os.environ['DWOLLA_APP_SECRET'])
```

### Using the sandbox environment (optional)

```python
client = dwollav2.Client(
  key = os.environ['DWOLLA_APP_KEY'],
  secret = os.environ['DWOLLA_APP_SECRET'],
  environment = 'sandbox'
)
```

`environment` defaults to `'production'`.

### Configure an `on_grant` callback (optional)

An `on_grant` callback is useful for storing new tokens when they are granted. The `on_grant`
callback is called with the `Token` that was just granted by the server.

```python
client = dwollav2.Client(
  key = os.environ['DWOLLA_APP_KEY'],
  secret = os.environ['DWOLLA_APP_SECRET'],
  on_grant = lambda t: save(t)
)
```

It is highly recommended that you encrypt any token data you store.

## `Token`

Tokens can be used to make requests to the Dwolla V2 API. There are two types of tokens:

### Application tokens

Application tokens are used to access the API on behalf of a consumer application. API resources that
belong to an application include: `webhook-subscriptions`, `events`, and `webhooks`. Application
tokens can be created using the [`client_credentials`][client_credentials] OAuth grant type:

[client_credentials]: https://tools.ietf.org/html/rfc6749#section-4.4

**Note:** If an application has the `ManageCustomers` scope enabled, it can also be used to access
the API for White Label Customer related endpoints. Keep in mind, the application must belong to
same Dwolla account that will be used when creating and managing White Label Customers in the API.

```python
application_token = client.Auth.client()
```

*Application tokens do not include a `refresh_token`. When an application token expires, generate
a new one using `client.Auth.client()`.*

### Account tokens

Account tokens are used to access the API on behalf of a Dwolla account. API resources that belong
to an account include `customers`, `funding-sources`, `documents`, `mass-payments`, `mass-payment-items`,
`transfers`, and `on-demand-authorizations`.

There are two ways to get an account token. One is by generating a token at
https://sandbox.dwolla.com/applications (sandbox) or https://www.dwolla.com/applications (production).

You can instantiate a generated token by doing the following:

```python
account_token = client.Token(access_token = '...', refresh_token = '...')
```

The other way to get an account token is using the [`authorization_code`][authorization_code]
OAuth grant type. This flow works by redirecting a user to dwolla.com in order to get authorization
and sending them back to your website with an authorization code which can be exchanged for a token.
For example:

[authorization_code]: https://tools.ietf.org/html/rfc6749#section-4.1

For more information see the [Request User Authorization][rua] section of the Dwolla V2 docs.

[rua]: https://docsv2.dwolla.com/#request-user-authorization

```python
# http://www.twobotechnologies.com/blog/2014/02/importance-of-state-in-oauth2.html
state = binascii.b2a_hex(os.urandom(15))
auth = client.Auth(redirect_uri = 'https://yoursite.com/callback',
                   scope = 'ManageCustomers|Funding',
                   state = state, # optional
                   verified_account = True, # optional
                   dwolla_landing = 'register') # optional

# redirect the user to dwolla.com for authorization
redirect_to(auth.url)

# exchange the code for a token using the variables provided to the redirect_uri in the query string
token = auth.callback(req.GET)
```

### Refreshing tokens

Tokens with a `refresh_token` can be refreshed using `client.Auth.refresh`, which takes a
`Token` as its first argument and returns a new token.

```python
new_token = client.Auth.refresh(expired_token)
```

### Initializing pre-existing tokens:

`Token`s can be initialized with the following attributes:

```python
client.Token(access_token = '...',
             refresh_token = '...',
             expires_in = 123,
             scope = '...',
             account_id = '...')
```

## Requests

`Token`s can make requests using the `#get`, `#post`, and `#delete` methods.

```python
# GET api.dwolla.com/resource?foo=bar
token.get('resource', foo = 'bar')

# POST api.dwolla.com/resource {"foo":"bar"}
token.post('resource', foo = 'bar')

# POST api.dwolla.com/resource multipart/form-data foo=...
token.post('resource', foo = ('mclovin.jpg', open('mclovin.jpg', 'rb'), 'image/jpeg'))

# PUT api.dwolla.com/resource {"foo":"bar"}
token.put('resource', foo = 'bar')

# DELETE api.dwolla.com/resource
token.delete('resource')
```

#### Setting headers

To set additional headers on a request you can pass a `dict` of headers as the 3rd argument.

For example:

```python
token.post('customers', { 'firstName': 'John', 'lastName': 'Doe', 'email': 'jd@doe.com' },
                        { 'Idempotency-Key': 'a52fcf63-0730-41c3-96e8-7147b5d1fb01' })
```

## Responses

Requests return a `Response`.

```python
res = token.get('/')

res.status
# => 200

res.headers
# => {'server'=>'cloudflare-nginx', 'date'=>'Mon, 28 Mar 2016 15:30:23 GMT', 'content-type'=>'application/vnd.dwolla.v1.hal+json; charset=UTF-8', 'content-length'=>'150', 'connection'=>'close', 'set-cookie'=>'__cfduid=d9dcd0f586c166d36cbd45b992bdaa11b1459179023; expires=Tue, 28-Mar-17 15:30:23 GMT; path=/; domain=.dwolla.com; HttpOnly', 'x-request-id'=>'69a4e612-5dae-4c52-a6a0-2f921e34a88a', 'cf-ray'=>'28ac1f81875941e3-MSP'}

res.body['_links']['events']['href']
# => 'https://api-sandbox.dwolla.com/events'
```

## Errors

If the server returns an error, a `dwollav2.Error` (or one of its subclasses) will be raised.
`dwollav2.Error`s are similar to `Response`s.

```python
try:
  token.get('/not-found')
except dwollav2.NotFoundError:
  e.status
  # => 404

  e.headers
  # => {"server"=>"cloudflare-nginx", "date"=>"Mon, 28 Mar 2016 15:35:32 GMT", "content-type"=>"application/vnd.dwolla.v1.hal+json; profile=\"http://nocarrier.co.uk/profiles/vnd.error/\"; charset=UTF-8", "content-length"=>"69", "connection"=>"close", "set-cookie"=>"__cfduid=da1478bfdf3e56275cd8a6a741866ccce1459179332; expires=Tue, 28-Mar-17 15:35:32 GMT; path=/; domain=.dwolla.com; HttpOnly", "access-control-allow-origin"=>"*", "x-request-id"=>"667fca74-b53d-43db-bddd-50426a011881", "cf-ray"=>"28ac270abca64207-MSP"}

  e.body.code
  # => "NotFound"
except dwollav2.Error:
  # ...
```

### `dwollav2.Error` subclasses:

*See https://docsv2.dwolla.com/#errors for more info.*

- `dwollav2.AccessDeniedError`
- `dwollav2.InvalidCredentialsError`
- `dwollav2.NotFoundError`
- `dwollav2.BadRequestError`
- `dwollav2.InvalidGrantError`
- `dwollav2.RequestTimeoutError`
- `dwollav2.ExpiredAccessTokenError`
- `dwollav2.InvalidRequestError`
- `dwollav2.ServerError`
- `dwollav2.ForbiddenError`
- `dwollav2.InvalidResourceStateError`
- `dwollav2.TemporarilyUnavailableError`
- `dwollav2.InvalidAccessTokenError`
- `dwollav2.InvalidScopeError`
- `dwollav2.UnauthorizedClientError`
- `dwollav2.InvalidAccountStatusError`
- `dwollav2.InvalidScopesError`
- `dwollav2.UnsupportedGrantTypeError`
- `dwollav2.InvalidApplicationStatusError`
- `dwollav2.InvalidVersionError`
- `dwollav2.UnsupportedResponseTypeError`
- `dwollav2.InvalidClientError`
- `dwollav2.MethodNotAllowedError`
- `dwollav2.ValidationError`
- `dwollav2.TooManyRequestsError`
- `dwollav2.ConflictError`

## Development

After checking out the repo, run `pip install -r requirements.txt` to install dependencies.
Then, run `python setup.py test` to run the tests.

To install this gem onto your local machine, run `pip install -e .`.

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/Dwolla/dwolla-v2-python.

## License

The package is available as open source under the terms of the [MIT License](https://github.com/Dwolla/dwolla-v2-python).

## Changelog

- **1.2.3** Check if IOBase when checking to see if something is a file.
- **1.2.2** Strip domain from URLs provided to token.* methods.
- **1.2.1** Update sandbox URLs from uat => sandbox.
- **1.2.0** Refer to Client id as key.
- **1.1.8** Support `verified_account` and `dwolla_landing` auth flags
- **1.1.7** Use session over connections for [performance improvement](http://docs.python-requests.org/en/master/user/advanced/#session-objects) ([#8](https://github.com/Dwolla/dwolla-v2-python/pull/8) - Thanks @bfeeser!)
- **1.1.5** Fix file upload bug when using with Python 2 ([#6](https://github.com/Dwolla/dwolla-v2-python/issues/6))
- **1.1.2** Add `TooManyRequestsError` and `ConflictError`
- **1.1.1** Add MANIFEST.in
- **1.1.0** Support per-request headers

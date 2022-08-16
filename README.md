# Dwolla SDK for Python

This repository contains the source code for Dwolla's Python-based SDK, which allows developers to interact with Dwolla's server-side API via a Python API. Any action that can be performed via an HTTP request can be made using this SDK when executed within a server-side environment.

## Table of Contents 

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Initialization](#initialization)
    - [Tokens](#tokens)
- [Making Requests](#making-requests)
  - [Low-level Requests](#low-level-requests)
    - [Setting Headers](#setting-headers)
    - [Responses](#responses)
      - [Success](#success)
      - [Error](#error)
- [Changelog](#changelog)
- [Community](#community)
- [Additional Resources](#additional-resources)

---

## Getting Started

### Installation

To begin using this SDK, you will first need to download it to your machine. We use [PyPi](https://pypi.python.org/pypi/dwollav2) to distribute this package from where you can automagically download it via [pip](https://pip.pypa.io/en/stable/installing/).

```
pip install dwollav2
```

### Initialization

Before any API requests can be made, you must first determine which environment you will be using, as well as fetch the application key and secret. To fetch your application key and secret, please visit one of the following links:

* Production: https://dashboard.dwolla.com/applications
* Sandbox: https://dashboard-sandbox.dwolla.com/applications

Finally, you can create an instance of `Client` with `key` and `secret` replaced with the application key and secret that you fetched from one of the aforementioned links, respectively.

```python
client = dwollav2.Client(
  key = os.environ['DWOLLA_APP_KEY'],
  secret = os.environ['DWOLLA_APP_SECRET'],
  environment = 'sandbox', # defaults to 'production'
  requests = {'timeout': 0.001}
)
```

##### Configure an `on_grant` callback (optional)

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

#### Tokens

##### Generating New Access Tokens

Application access tokens are used to authenticate against the API on behalf of an application. Application tokens can be used to access resources in the API that either belong to the application itself (`webhooks`, `events`, `webhook-subscriptions`) or the Dwolla Account that owns the application (`accounts`, `customers`, `funding-sources`, etc.). Application tokens are obtained by using the [`client_credentials`][client_credentials] OAuth grant type:

[client_credentials]: https://tools.ietf.org/html/rfc6749#section-4.4

```python
application_token = client.Auth.client()
```

_Application access tokens are short-lived: 1 hour. They do not include a `refresh_token`. When it expires, generate a new one using `client.Auth.client()`._

##### Initializing Pre-Existing Tokens:

The [Dwolla Sandbox Dashboard](https://dashboard-sandbox.dwolla.com/applications-legacy) allows you to generate `token`s for your application. These tokens can be initialized with the following attributes:

```python
client.Token(access_token = '...',
             expires_in = 123)
```

## Making Requests

Once you've created a `token`, currently, you can make low-level HTTP requests.

### Low-level Requests

To make low-level HTTP requests, you can use the `get()`, `post()`, and `delete()` methods. These methods will return a `Response` object.

#### `GET`
```python
# GET api.dwolla.com/resource?foo=bar
token.get('resource', foo = 'bar')

# GET requests can also use objects as parameters
# GET api.dwolla.com/resource?foo=bar
token.get('resource', {'foo' = 'bar', 'baz' = 'foo'})
```

#### `POST`
```python
# POST api.dwolla.com/resource {"foo":"bar"}
token.post('resource', foo = 'bar')

# POST api.dwolla.com/resource multipart/form-data foo=...
token.post('resource', foo = ('mclovin.jpg', open('mclovin.jpg', 'rb'), 'image/jpeg'))
```

#### `DELETE`
```python
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

#### Responses

The following snippets demonstrate successful and errored responses from the Dwolla API.

An errored response is returned when Dwolla's servers respond with a status code that is greater than or equal to 400, whereas a successful response is when Dwolla's servers respond with a 200-level status code.


##### Success
```python
res = token.get('/')

res.status
# => 200

res.headers
# => {'server'=>'cloudflare-nginx', 'date'=>'Mon, 28 Mar 2016 15:30:23 GMT', 'content-type'=>'application/vnd.dwolla.v1.hal+json; charset=UTF-8', 'content-length'=>'150', 'connection'=>'close', 'set-cookie'=>'__cfduid=d9dcd0f586c166d36cbd45b992bdaa11b1459179023; expires=Tue, 28-Mar-17 15:30:23 GMT; path=/; domain=.dwolla.com; HttpOnly', 'x-request-id'=>'69a4e612-5dae-4c52-a6a0-2f921e34a88a', 'cf-ray'=>'28ac1f81875941e3-MSP'}

res.body['_links']['events']['href']
# => 'https://api-sandbox.dwolla.com/events'
```

##### Error

If the server returns an error, a `dwollav2.Error` (or one of its subclasses) will be raised.
`dwollav2.Error`s are similar to `Response`s.

```python
try:
  token.get('/not-found')
except dwollav2.NotFoundError as e:
  e.status
  # => 404

  e.headers
  # => {"server"=>"cloudflare-nginx", "date"=>"Mon, 28 Mar 2016 15:35:32 GMT", "content-type"=>"application/vnd.dwolla.v1.hal+json; profile=\"http://nocarrier.co.uk/profiles/vnd.error/\"; charset=UTF-8", "content-length"=>"69", "connection"=>"close", "set-cookie"=>"__cfduid=da1478bfdf3e56275cd8a6a741866ccce1459179332; expires=Tue, 28-Mar-17 15:35:32 GMT; path=/; domain=.dwolla.com; HttpOnly", "access-control-allow-origin"=>"*", "x-request-id"=>"667fca74-b53d-43db-bddd-50426a011881", "cf-ray"=>"28ac270abca64207-MSP"}

  e.body.code
  # => "NotFound"
except dwollav2.Error:
  # ...
```
###### `dwollav2.Error` subclasses:

_See https://developers.dwolla.com/api-reference#errors for more info._

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

## Changelog

- **2.2.1**
  - Add extra check in URL's to ensure they are clean. [#36](https://github.com/Dwolla/dwolla-v2-python/pull/36).
- **2.2.0**
  - Update JSON request bodies to serialize via `simplejson` so datatypes like `Decimal` still
    serialize like they did pre `2.0.0`
- **2.1.0**
  - Do not share `requests.session()` across instances of `dwollav2.Client`
- **2.0.0**
  - JSON request bodies now contain sorted keys to ensure the same request body for a given set of
    arguments, no matter the order they are passed to `dwolla.post`. This ensures the
    [`Idempotency-Key`][] header will work as intended without additional effort by developers.
  - **NOTE**: Because this change alters the formatting of JSON request bodies, we are releasing it
    as a major new version. The request body of a request made with `1.6.0` will not match the
    request body of the same request made in `2.0.0`. This will nullify the effect of the
    [`Idempotency-Key`][] header when upgrading, so please take this into account.
    If you have any questions please [reach out to us](https://discuss.dwolla.com/)!
    There are no other changes since `1.6.0`.
- **1.6.0** Allow configuration of `requests` options on `dwollav2.Client`.
- **1.5.0** Add integrations auth functionality
- **1.4.0** ~~Pass kwargs from `get`, `post`, and `delete` methods to underlying requests methods.~~ (Removed in v1.6)
- **1.3.0** Change token URLs, update dependencies.
- **1.2.4** Create a new session for each Token.
- **1.2.3** Check if IOBase when checking to see if something is a file.
- **1.2.2** Strip domain from URLs provided to token.\* methods.
- **1.2.1** Update sandbox URLs from uat => sandbox.
- **1.2.0** Refer to Client id as key.
- **1.1.8** Support `verified_account` and `dwolla_landing` auth flags
- **1.1.7** Use session over connections for [performance improvement](http://docs.python-requests.org/en/master/user/advanced/#session-objects) ([#8](https://github.com/Dwolla/dwolla-v2-python/pull/8) - Thanks [@bfeeser](https://github.com/bfeeser)!
- **1.1.5** Fix file upload bug when using with Python 2 ([#6](https://github.com/Dwolla/dwolla-v2-python/issues/6))
- **1.1.2** Add `TooManyRequestsError` and `ConflictError`
- **1.1.1** Add MANIFEST.in
- **1.1.0** Support per-request headers

## Community
* If you have any feedback, please reach out to us on [our forums](https://discuss.dwolla.com/) or by [creating a GitHub issue](https://github.com/Dwolla/dwolla-v2-python/issues/new).
* If you would like to contribute to this library, bug reports and pull requests are welcome on GitHub at https://github.com/Dwolla/dwolla-v2-python.
  * After checking out the repo, run `pip install -r requirements.txt` to install dependencies. Then, run `python setup.py` test to run the tests. 
  * To install this gem onto your local machine, `run pip install -e .`.
  

## Additional Resources

To learn more about Dwolla and how to integrate our product with your application, please consider visiting the following resources and becoming a member of our community!

* [Dwolla](https://www.dwolla.com/)
* [Dwolla Developers](https://developers.dwolla.com/)
* [SDKs and Tools](https://developers.dwolla.com/sdks-tools)
  * [Dwolla SDK for C#](https://github.com/Dwolla/dwolla-v2-csharp)
  * [Dwolla SDK for Kotlin](https://github.com/Dwolla/dwolla-v2-kotlin)
  * [Dwolla SDK for Node](https://github.com/Dwolla/dwolla-v2-node)
  * [Dwolla SDK for Ruby](https://github.com/Dwolla/dwolla-v2-ruby)
* [Developer Support Forum](https://discuss.dwolla.com/)

---

[`idempotency-key`]: https://docs.dwolla.com/#idempotency-key

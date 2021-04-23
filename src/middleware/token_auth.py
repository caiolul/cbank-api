from starlette_jwt import JWTAuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware import Middleware
from starlette.config import Config

key = Config('.env')


def middleware_token():
    back_token = JWTAuthenticationBackend(
        secret_key=key('HASH_GEN'), username_field='email')

    mid = [Middleware(AuthenticationMiddleware, backend=back_token)]
    return mid

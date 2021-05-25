from starlette_jwt import JWTAuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.config import Config
from starlette.middleware import Middleware

key = Config('.env')


def middleware_token():
    back_token = JWTAuthenticationBackend(
        secret_key=key('HASH_GEN'), username_field='email', prefix='JWT')

    mid = [Middleware(AuthenticationMiddleware, backend=back_token),
           Middleware(CORSMiddleware, allow_origins=['*']), ]
    return mid

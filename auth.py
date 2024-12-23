import os
import json
import urllib.request
from functools import wraps
from flask import request, jsonify, _request_ctx_stack
from jose import jwt
from settings import AUTH0_DOMAIN, ALGORITHMS, API_IDENTIFIER


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def verify_decode_jwt(token):
    try:
        jsonurl = urllib.request.urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_IDENTIFIER,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 401)
    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)
    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims. Check the audience and issuer.'
        }, 401)
    except Exception:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth = request.headers.get('Authorization', None)
            if not auth:
                raise AuthError({
                    'code': 'authorization_header_missing',
                    'description': 'Authorization header is expected.'
                }, 401)
            parts = auth.split()
            if parts[0].lower() != 'bearer':
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Authorization header must start with Bearer.'
                }, 401)
            elif len(parts) == 1:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Token not found.'
                }, 401)
            elif len(parts) > 2:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Authorization header must be Bearer token.'
                }, 401)

            token = parts[1]
            payload = verify_decode_jwt(token)
            if permission not in payload.get('permissions', []):
                raise AuthError({
                    'code': 'unauthorized',
                    'description': 'Permission not found.'
                }, 403)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

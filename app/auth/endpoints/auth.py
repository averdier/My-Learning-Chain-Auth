# -*- coding: utf-8 -*-

import time
import jwt
from flask import g, request, current_app
from flask_restplus import Namespace, Resource, abort, marshal
from ..serializers.auth import jwks_model, access_token, verify_token_parameters, token_model, user_full_resource
from ..parsers import auth_parser
from .. import auth
from app.models import User


ns = Namespace('auth', description='Auth related operations.')


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API Auth endpoints
#
# ================================================================================================


def is_authorized_client(username, secret):
    """
    Verify if is authorized client

    :param username:
    :param secret:
    :return:
    """
    u = User.objects(username=username).first()

    if u is None:
        return False

    if u.check_secret(secret):
        g.client = u
        return True

    return False


@ns.route('/token')
class TokenGenerator(Resource):

    @ns.marshal_with(access_token)
    @ns.expect(auth_parser)
    def post(self):
        """
        Get token
        """
        data = request.form

        audience = ''

        if not is_authorized_client(data['username'], data['secret']):
            abort(401, error='Unauthorized')

        now = int(time.time())

        token = {
            'iss': 'https://localhost/public/auth',
            'aud': audience,
            'iat': now,
            'exp': now + 3600 * 24,
            'user': marshal(g.client, user_full_resource)
        }

        token = jwt.encode(token, current_app.config['PRIVATE_KEY'], algorithm='RS512')

        return {'access_token': token.decode('utf-8')}


@ns.route('/verify_token')
class TokenVerifier(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(token_model)
    @ns.expect(verify_token_parameters)
    def post(self):
        """
        Verify token
        """
        data = request.json

        try:
            return jwt.decode(
                data['access_token'],
                current_app.config['PUBLIC_KEY'],
                audience=''
            )
        except Exception as ex:
            print(ex)
            abort(400, 'Invalid token')


@ns.route('/.well-known/jwks.json')
class WellKnown(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(jwks_model)
    def get(self):
        """
        Return public key in JWK
        """
        try:
            key = {
                'alg': 'RS512',
                'e': 'AQAB',
                'n': current_app.config['PUBLIC_KEY'],
                'kty': 'RSA',
                'use': 'SIG'
            }

            return key

        except Exception as ex:
            abort(400, error='{0}'.format(ex))





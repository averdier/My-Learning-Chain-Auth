# -*- coding: utf-8 -*-

from flask_restplus import fields
from .. import api

campus_nested = api.model('Campus nested', {
    'id': fields.String(required=True, description='Campus ID'),
    'name': fields.String(required=True, description='Name')
})

user_resource = api.model('User resource', {
    'id': fields.String(required=True, description='User ID'),
    'type': fields.String(required=True, description='Type'),
    'campus': fields.Nested(campus_nested, required=True, allow_null=True, description='Campus'),
    'username': fields.String(required=True, description='Username'),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Last name")
})

user_full_resource = api.inherit('User full resource', user_resource, {
    'scopes': fields.List(fields.String(), required=True, description='User scopes')
})

jwks_model = api.model('jwks.json model', {
    'alg': fields.String(required=True, description='Algorithm'),
    'e': fields.String(required=True, description='?'),
    'n': fields.String(required=True, description='Public key'),
    'kty': fields.String(required=True, description='?'),
    'use': fields.String(required=True, description='?')
})

token_model = api.model('Token model', {
    'iss': fields.String(required=True, desctiption='Issuer'),
    'aud': fields.String(required=True, description='Audience'),
    'iat': fields.Integer(required=True, description='Issued at'),
    'exp': fields.Integer(required=True, description='Expiration time'),
    'user': fields.Nested(user_full_resource, required=True, description='User')
})


access_token = api.model('Access token', {
    'access_token': fields.String(required=True, description='Token')
})

verify_token_parameters = api.model('Verify token parameters', {
    'access_token': fields.String(required=True, description='Token')
})

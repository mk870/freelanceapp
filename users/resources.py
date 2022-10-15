from flask import jsonify
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended import jwt_required

from security import password_validator

from .models import UserModel
from .schema import user_schema

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="username cannot be empty"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="password cannot be empty"
                          )


class UserSignUp(Resource):
    def post(self):
        data = _user_parser.parse_args()
        username = data['username']
        password = data['password']

        if UserModel.find_by_username(username):
            return {'error': f"user {username} already exists"}, 400

        if not password_validator.validate(password):
            return {'error': 'password too weak'}, 400

        password_hash = generate_password_hash(password)
        user = UserModel(**data)
        user.password = password_hash
        user.save()

        return {'ok': 'user created'}, 201


class UserSignIn(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        username = data['username']
        password = data['password']

        user = UserModel.find_by_username(username)

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user_schema.dump(user)
            }

        return {'error': 'invalid credentials'}, 401


class UsersResource(Resource):

    @jwt_required()
    # @classmethod
    def get(self):
        user = UserModel.find_by_id(get_jwt_identity())
        if user:
            return jsonify(user_schema.dump(user))

        return {'error': 'user not found'}, 404

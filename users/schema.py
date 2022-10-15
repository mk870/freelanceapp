from marshmallow import fields
from db import ma
from .models import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        Model = UserModel
        load_instance = True

    id = fields.Integer()
    username = fields.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)

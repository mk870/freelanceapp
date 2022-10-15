from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import enum

db = SQLAlchemy()

ma = Marshmallow()

# sex enum


class SexEnum(str, enum.Enum):
    male = 'male'
    female = 'female'

# empoyee types enum


class EmployeeTypeEnum(str, enum.Enum):
    marshal = 'marshal'
    enforcement = 'enforcement'
    admin = 'admin'

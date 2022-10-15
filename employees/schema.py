from marshmallow_enum import EnumField

from db import ma, SexEnum
from .models import EmployeeModel


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    type = EnumField(SexEnum, by_value=True)

    class Meta:
        model = EmployeeModel
        load_instance = True


employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

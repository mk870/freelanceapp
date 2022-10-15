from sqlalchemy.sql import func

from db import db, SexEnum, EmployeeTypeEnum


class EmployeeModel(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False, index=True)
    last_name = db.Column(db.String(80), nullable=False, index=True)
    sex = db.Column(db.Enum(SexEnum), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    id_number = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())
    employee_type = db.Column(db.Enum(EmployeeTypeEnum), nullable=False)

    @classmethod
    def get_by_name(cls, first_name, last_name):
        return cls.query.filter_by(first_name=first_name, last_name=last_name).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

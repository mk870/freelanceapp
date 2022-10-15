from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from urllib.parse import urlparse, parse_qs


from .models import EmployeeModel
from .schema import employee_schema, employees_schema


class Employee(Resource):
    @jwt_required()
    def get(self, id):
        employee = EmployeeModel.get_by_id(id)
        if employee:
            return jsonify(employee_schema.dump(employee))

        return {'error': 'employee not found'}, 404

    @jwt_required()
    def delete(self, id):
        employee = EmployeeModel.get_by_id(id)

        if employee:
            employee.delete()
            return {'ok': 'deleted'}
        return {'error', 'employee you are trying to delete does not exist'}

    @jwt_required()
    def put(self, id):
        employee = EmployeeModel.get_by_id(id)
        update_data = {k: v for k, v in request.get_json().items()
                       if v is not None}

        for key, value in update_data.items():
            setattr(employee, key, value)

        employee.save()

        return employee_schema.dump(employee)


class EmployeeList(Resource):
    @jwt_required()
    def post(self):
        # or create an obj and return it after a successful post or put
        data = request.get_json()
        first_name = data['first_name']
        last_name = data['last_name']

        if EmployeeModel.get_by_name(first_name, last_name):
            return {'error': f"Employee {first_name} {last_name} already exists"}

        employee = EmployeeModel(**data)

        try:
            employee.save()
        except Exception as e:
            return {'error': 'error saving employee'}, 500

        return employee_schema.dump(employee), 201

    @jwt_required()
    def get(self):
        first_name = request.args.get('first_name') or ''
        page = int(request.args.get('page') or 1)
        search = "%{}%".format(first_name)

        data = EmployeeModel.query.filter(EmployeeModel.first_name.ilike(search)).order_by(
            EmployeeModel.created_at.desc()).paginate(page=page, per_page=8)

        pagination = {
            "page": data.page,
            "pages": data.pages,
            "total_count": data.total,
            "prev_page": data.prev_num,
            "has_next": data.has_next,
            "has_prev": data.has_prev
        }

        return jsonify({"data": employees_schema.dump(data.items), "pagination": pagination})

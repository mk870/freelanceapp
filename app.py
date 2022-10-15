from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS


from users.resources import UserSignUp, UserSignIn, UsersResource
from employees.resources import Employee, EmployeeList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fjytmlxs:w1u4JkUBdCxFf0iVBFUlb6tdwGDD6BA4@lucky.db.elephantsql.com/fjytmlxs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

app.secret_key = 'tti-admin-secret'  # store secret somewhere
api = Api(app)
CORS(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)

api.add_resource(UserSignIn, '/sign_in')
api.add_resource(UserSignUp, '/sign_up')
api.add_resource(UsersResource, '/current_session')
api.add_resource(Employee, '/employees/<int:id>')
api.add_resource(EmployeeList, '/employees', endpoint='employees')


if __name__ == '__main__':
    from db import db, ma

    db.init_app(app)
    ma.init_app(app)
    app.run(debug=True)

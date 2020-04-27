import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

path_to_db = r'C:\Users\raksh\PycharmProjects\Flask project\data.db'


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="Fields are required.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Fields are required.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "user already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201

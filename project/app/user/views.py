from datetime import datetime
from extensions import app, Session
from flask import request, jsonify
from .models import User
from .schema import UserSchema, UserSchemaUpdate
from .schema import UserLoginSchema
from imports import *
from admin_dec import *


@app.route('/user', methods=['POST', 'GET'])
def create_user():
    session = Session()

    if request.method == 'POST':
        try:
            user_data = UserSchema().load(request.json)

            if session.query(User).filter_by(phone=user_data['phone']).first():
                content = jsonify({"Error": "Phone is not unique"})
                return content, 405, {'content-type': 'application/json'}
            elif session.query(User).filter_by(
                    email=user_data['email']).first():
                content = jsonify({"Error": "Email is not unique"})
                return content, 405, {'content-type': 'application/json'}
            else:
                my_post = User(**request.json)
                session.add(my_post)
                session.commit()
                session.expunge_all()
                return UserSchema().jsonify(user_data)

        except ValidationError as e:
            rv = e.normalized_messages()
            return rv, 400, {'content-type': 'application/json'}

    elif request.method == 'GET':
        users = session.query(User).all()
        if not users:
            content = jsonify({"Error": "Database is empty"})
            return content, 404, {'content-type': 'application/json'}
        else:
            return UserSchema(many=True).jsonify(users)


@app.route('/user/<id>', methods=['GET'])
@jwt_required()
@admin_required
def user_get(id):
    session = Session()
    user_data = session.query(User).get(id)

    if user_data:
        if request.method == 'GET':
            return UserSchema().jsonify(user_data)
    else:
        content = jsonify({"Error": "User doesn't exists"})
        return content, 404, {'content-': 'application/json'}


@app.route('/user/<id>', methods=['PUT', 'DELETE'])
@jwt_required()
# @admin_required
def user(id):
    session = Session()
    current_identity_email = get_jwt_identity()
    user_data = session.query(User).get(id)


    if user_data:
        if current_identity_email == user_data.email:
            if request.method == 'PUT':
                user_request = UserSchemaUpdate().load(request.json)

                user_data.first_name = user_request['first_name']
                user_data.last_name = user_request['last_name']

                if user_request['first_name'] != "" and \
                        user_request['last_name'] != "":
                    session.commit()
                    return UserSchemaUpdate().jsonify(user_data)
                else:
                    content = jsonify({"Error": "Fields can`t be empty"})
                    return content, 400, {'content-type': 'application/json'}

            elif request.method == 'DELETE':
                session.delete(user_data)
                session.commit()
                content = jsonify({"Success": "User was deleted"})
                return content, 200, {'content-type': 'application/json'}
        else:
            content = jsonify({"Error": "Access is denied"})
            return content, 404, {'content-': 'application/json'}
    else:
        content = jsonify({"Error": "User doesn't exists"})
        return content, 404, {'content-': 'application/json'}


@app.route('/user/login', methods=['GET'])
def login_user():
    session = Session()
    try:
        user_request = UserLoginSchema().load(request.json)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if not user_request:
        content = jsonify({"Error": "could not verify user_request"})
        return content, 401, {'content-': 'application/json'}

    user = session.query(User).filter_by(email=user_request['email']).first()

    if user and check_password_hash(user.password, user_request['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify({'token': access_token})

    content = jsonify({"Error": "could not verify"})
    return content, 401, {'content-': 'application/json'}

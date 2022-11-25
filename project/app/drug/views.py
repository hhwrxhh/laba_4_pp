from extensions import app, Session
from flask import request, jsonify
from .models import Dosed
from .schema import DosedSchema, DosedSchemaUpdate
from .schema import UserGetId
from ..user.models import User
from imports import *
from admin_dec import *

@app.route('/drug/add/dosed', methods=['POST'])
@jwt_required()
@admin_required
def dosed_post():
    session = Session()
    try:
        dosed_request = DosedSchema().load(request.json)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}


    if request.method == 'POST':
        try:
            my_post = Dosed(**request.json)
            session.add(my_post)
            session.commit()
            return DosedSchema().jsonify(my_post)
        except ValidationError as e:
            rv = dict({'message': e.normalized_messages()})
            return rv, 400, {'content-type': 'application/json'}
        except OperationalError as e:
            rv = dict({'message': "One of the fields is empty"})
            return rv, 404, {'content-type': 'application/json'}
        except IntegrityError as e:
            session.rollback()
            #errorInfo = e.orig.args
            rv = dict({'message': "one of the fk is not valid"})
            return rv, 400, {'content-type': 'application/json'}


@app.route('/drug/dosed/<id>',
           methods=['GET'])
def dosed_pdg(id):
    session = Session()
    dosed_data = session.query(Dosed).filter_by(
        dosed_id=id).first()

    if dosed_data:
        if request.method == 'GET':
            return DosedSchema().jsonify(dosed_data)
    else:
        content = jsonify({"Error": "Dosed  doesn't exists"})
        return content, 404, {'content-': 'application/json'}


@app.route('/drug/dosed/<id>',
           methods=['PUT', 'DELETE'])
@jwt_required()
@admin_required
def dosed_pd(id):
    session = Session()
    dosed_data = session.query(Dosed).filter_by(
        dosed_id=id).first()


    if dosed_data:
        if request.method == 'PUT':

            try:
                dosed_request = DosedSchemaUpdate().load(request.json)
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}

            try:
                dosed_data.dosed_name = dosed_request[
                    'dosed_name']
                dosed_data.dosed_description = dosed_request[
                    'dosed_description']
                session.commit()
                return DosedSchemaUpdate().jsonify(dosed_data)
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
            except IntegrityError as e:
                session.rollback()
                errorInfo = e.orig.args
                rv = dict({'message': errorInfo[1]})
                return rv, 400, {'content-type': 'application/json'}

        elif request.method == 'DELETE':

            session.delete(dosed_data)
            session.commit()
            content = jsonify({"Success": "dosed_data was deleted"})
            return content, 200, {'content-type': 'application/json'}

    else:
        content = jsonify({"Error": "Dosed  doesn't exists"})
        return content, 404, {'content-': 'application/json'}

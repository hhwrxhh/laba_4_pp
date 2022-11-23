from extensions import app, Session
from flask import request, jsonify
from .models import Producer
from .schema import ProducerSchema
from imports import *


@app.route('/producer', methods=['POST'])
def producer_post():
    session = Session()
    try:
        rpoducer_data = ProducerSchema().load(request.json)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}
    if request.method == 'POST':
        try:
            my_post = Producer(**request.json)
            session.add(my_post)
            session.commit()
            return ProducerSchema().jsonify(my_post)
        except ValidationError as e:
            rv = dict({'message': e.normalized_messages()})
            return rv, 400, {'content-type': 'application/json'}
        except IntegrityError as e:
            session.rollback()
            errorInfo = e.orig.args
            rv = dict({'message': errorInfo[1]})
            return rv, 400, {'content-type': 'application/json'}


@app.route('/producer/<id>', methods=['PUT', 'DELETE'])
def producer_pd(id):
    session = Session()
    producer_data = session.query(Producer).get(id)

    if producer_data:
        if request.method == 'PUT':
            try:
                producer_request = ProducerSchema().load(request.json)
                producer_data.producing_company = producer_request[
                    'producing_company']
                producer_data.producing_country = producer_request[
                    'producing_country']
                session.commit()
                return ProducerSchema().jsonify(producer_request)
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
        elif request.method == 'DELETE':
            session.delete(producer_data)
            session.commit()
            content = jsonify({"Success": "Producer was deleted"})
            return content, 200, {'content-type': 'application/json'}
    else:
        content = jsonify({"Error": "Producer doesn't exists"})
        return content, 404, {'content-': 'application/json'}



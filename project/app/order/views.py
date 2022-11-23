from extensions import app, Session
from flask import request, jsonify
from .models import Order
from .schema import OrderSchema, OrderSchemaUpdate
from .schema import UserGetId, OrderSchemaGet

from ..cart.models import Cart
from ..user.models import User
from ..drug.models import Dosed

from imports import *


@app.route('/order', methods=['POST'])
def order_post_get():
    session = Session()

    try:
        order_data = OrderSchema().load(request.json)
        tmp = request.json['fk_cart_id']
        user_id = request.json['fk_user_id']
        cart_data = session.query(Cart).filter_by(
            cart_id=tmp, fk_user_id=user_id).first()
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if cart_data:
        if request.method == 'POST':
            try:
                result = Dosed.query.with_entities(
                    func.sum(Dosed.dosed_price).label("mySum")
                ).filter_by(
                    dosed_id=cart_data.fk_dosed_id
                )
                request.json['total'] = result
                my_post = Order(**request.json)
                session.add(my_post)
                session.commit()
                return OrderSchema().jsonify(my_post)
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}

            except IntegrityError as e:
                session.rollback()
                rv = dict({'message': "Cart/User doesn`t exist"})
                return rv, 400, {'content-type': 'application/json'}
    else:
        rv = dict({'message': "Cart/User doesn`t exist"})
        return rv, 400, {'content-type': 'application/json'}


@app.route('/order', methods=['GET'])
def order_get():
    session = Session()
    try:
        order_data = UserGetId().load(request.json)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if request.method == 'GET':
        q = session.query(Order).filter_by(
            fk_user_id=request.json['fk_user_id']).all()

        if not q:
            rv = dict({'message': "Orders are empty"})
            return rv, 400, {'content-type': 'application/json'}
        else:
            return OrderSchema(many=True).jsonify(q)


@app.route('/order/<id>', methods=['GET'])
def order_g(id):
    session = Session()
    try:
        order_request = OrderSchemaGet().load(request.json)
        order_data = session.query(Order).filter_by(
            order_id=id).first()
        use_id = order_request['fk_user_id']
        user_obj = session.query(User).get(use_id)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if user_obj:
        if order_data:
            if user_obj.user_id == order_data.fk_user_id:
                if request.method == 'GET':
                    return OrderSchemaGet().jsonify(order_data)
            else:
                content = jsonify(
                    {"Error": "You are not allowed to get an order"})
                return content, 404, {'content-': 'application/json'}
        else:
            content = jsonify({"Error": "Order doesn't exists"})
            return content, 404, {'content-': 'application/json'}
    else:
        content = jsonify({"Error": "User doesn't exists"})
        return content, 404, {'content-': 'application/json'}


@app.route('/order/<id>',
           methods=['PUT', 'DELETE'])
def order_pd(id):
    session = Session()
    order_data = session.query(Order).filter_by(
        order_id=id).first()

    if order_data:
        if request.method == 'PUT':
            try:
                order_request = OrderSchemaUpdate().load(request.json)

                use_id = order_request['fk_user_id']
                cart_id = order_request['fk_cart_id']

                user_obj = session.query(User).filter_by(
                    user_id=use_id).first()
                cart_data = session.query(Cart).filter_by(
                    cart_id=cart_id).first()
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
            if user_obj and cart_data:
                if user_obj.user_id == order_data.fk_user_id:
                    if order_data.fk_user_id == cart_data.fk_user_id:
                        try:
                            if 'fk_cart_id' in request.json:
                                order_data.fk_cart_id = order_request[
                                    'fk_cart_id']
                            else:
                                rv = dict({'message': "fk_cart_id is empty"})
                                return rv, 400, {
                                    'content-type': 'application/json'}
                            session.commit()
                            return OrderSchemaUpdate().jsonify(order_data)
                        except ValidationError as e:
                            rv = dict({'message': e.normalized_messages()})
                            return rv, 400, {'content-type': 'application/json'}
                        except IntegrityError as e:
                            session.rollback()
                            errorInfo = e.orig.args
                            rv = dict({'message': errorInfo[1]})
                            return rv, 400, {'content-type': 'application/json'}
                    else:
                        content = jsonify(
                            {"Error": "You don't have access to it"})
                        return content, 404, {'content-': 'application/json'}
                else:
                    content = jsonify({"Error": "You are not allowed"})
                    return content, 404, {'content-': 'application/json'}
            else:
                content = jsonify({"Error": "User/Cart not found"})
                return content, 404, {'content-': 'application/json'}

        elif request.method == 'DELETE':
            try:
                order_request = UserGetId().load(request.json)
                use_id = order_request['fk_user_id']
                user_obj = session.query(User).filter_by(
                    user_id=use_id).first()
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
            if user_obj:
                if user_obj.user_id == order_data.fk_user_id:
                    session.delete(order_data)
                    session.commit()
                    content = jsonify({"Success": "order was deleted"})
                    return content, 200, {'content-type': 'application/json'}
                else:
                    content = jsonify({"Error": "You are not allowed"})
                    return content, 404, {'content-': 'application/json'}
            else:
                content = jsonify({"Error": "User doen'nt exists"})
                return content, 404, {'content-': 'application/json'}

    else:
        content = jsonify({"Error": "order  doesn't exists"})
        return content, 404, {'content-': 'application/json'}

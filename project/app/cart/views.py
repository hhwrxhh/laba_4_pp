from extensions import app, Session
from flask import request, jsonify
from .models import Cart
from .schema import CartSchema, CartSchemaUpdate
from .schema import CartSchemaGet, UserGetId
from imports import *
from ..user.models import User


@app.route('/cart', methods=['POST'])
def cart_post_get():
    session = Session()

    try:
        cart_data = CartSchema().load(request.json)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if request.method == 'POST':
        try:
            my_post = Cart(**request.json)
            session.add(my_post)
            session.commit()
            return CartSchema().jsonify(my_post)
        except ValidationError as e:
            rv = dict({'message': e.normalized_messages()})
            return rv, 400, {'content-type': 'application/json'}
        except IntegrityError as e:
            session.rollback()
            rv = dict({'message': "Dosed/User don't exist"})
            return rv, 400, {'content-type': 'application/json'}

@app.route('/cart', methods=['GET'])
def cart_get():
    session = Session()
    try:
        cart_data = UserGetId().load(request.json)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if request.method == 'GET':
        q = session.query(Cart).filter_by(
            fk_user_id=request.json['fk_user_id']).all()

        if not q:
            rv = dict({'message': "Carts are empty"})
            return rv, 400, {'content-type': 'application/json'}
        else:
            return CartSchema(many=True).jsonify(q)



# @app.route('/cart/add_new/<cart_id>', methods=['POST', 'GET'])
# def cart_add_new(cart_id):
#     session = Session()
#     try:
#         cart_request = CartSchema().load(request.json)
#         cart_data = session.query(Cart).filter_by(
#             cart_id=cart_id).first()
#
#         use_id = cart_request['fk_user_id']
#         user_obj = session.query(User).get(use_id)
#
#     except ValidationError as e:
#         rv = dict({'message': e.normalized_messages()})
#         return rv, 400, {'content-type': 'application/json'}
#
#     if user_obj:
#         if user_obj.user_id == cart_data.fk_user_id:
#             if cart_data:
#                 if request.method == 'POST':
#                     try:
#                         request.json['cart_id'] = cart_id
#                         my_post = Cart(**request.json)
#                         session.add(my_post)
#                         session.commit()
#                         return CartSchema().jsonify(my_post)
#                     except ValidationError as e:
#                         rv = dict({'message': e.normalized_messages()})
#                         return rv, 400, {'content-type': 'application/json'}
#                     except IntegrityError as e:
#                         session.rollback()
#                         errorInfo = e.orig.args
#                         rv = dict({'message': errorInfo[1]})
#                         return rv, 400, {'content-type': 'application/json'}
#             else:
#                 content = jsonify({"Error": "Cart doesn't exists"})
#                 return content, 404, {'content-': 'application/json'}
#         else:
#             content = jsonify({"Error": "You are not allowed to add new to cart"})
#             return content, 404, {'content-': 'application/json'}
#     else:
#         content = jsonify({"Error": "User or drug don't exist "})
#         return content, 404, {'content-': 'application/json'}


@app.route('/cart/<id>', methods=['GET'])
def cart_g(id):
    session = Session()
    try:
        cart_request = CartSchemaGet().load(request.json)
        cart_data = session.query(Cart).filter_by(
            cart_id=id).first()

        use_id = cart_request['fk_user_id']
        user_obj = session.query(User).get(use_id)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if user_obj:
        if user_obj.user_id == cart_data.fk_user_id:
            if cart_data:
                if request.method == 'GET':
                    return CartSchemaGet().jsonify(cart_data)
            else:
                content = jsonify({"Error": "Cart doesn't exists"})
                return content, 404, {'content-': 'application/json'}
        else:
            content = jsonify({"Error": "You are not allowed to get a cart"})
            return content, 404, {'content-': 'application/json'}
    else:
        content = jsonify({"Error": "User doesn't exists"})
        return content, 404, {'content-': 'application/json'}


@app.route('/cart/<id>',
           methods=['PUT', 'DELETE'])
def cart_pd(id):
    session = Session()
    cart_data = session.query(Cart).filter_by(
        cart_id=id).first()

    if cart_data:
        if request.method == 'PUT':
            try:
                cart_request = CartSchemaUpdate().load(request.json)
                use_id = cart_request['fk_user_id']
                user_obj = session.query(User).filter_by(
                    user_id=use_id).first()
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}

            if user_obj:
                if user_obj.user_id == cart_data.fk_user_id:
                    try:
                        if 'fk_dosed_id' in request.json:
                            cart_data.fk_dosed_id = cart_request[
                                'fk_dosed_id']
                        else:
                            rv = dict({'message': "Cart is empty"})
                            return rv, 400, {'content-type': 'application/json'}
                        session.commit()
                        return CartSchemaUpdate().jsonify(cart_data)
                    except ValidationError as e:
                        rv = dict({'message': e.normalized_messages()})
                        return rv, 400, {'content-type': 'application/json'}
                    except IntegrityError as e:
                        session.rollback()
                        errorInfo = e.orig.args
                        rv = dict({'message': errorInfo[1]})
                        return rv, 400, {'content-type': 'application/json'}
                else:
                    content = jsonify({"Error": "You are not allowed"})
                    return content, 404, {'content-': 'application/json'}
            else:
                content = jsonify({"Error": "User doen'nt exists"})
                return content, 404, {'content-': 'application/json'}

        elif request.method == 'DELETE':
            cart_request = UserGetId().load(request.json)
            use_id = cart_request['fk_user_id']
            user_obj = session.query(User).filter_by(
                user_id=use_id).first()

            if user_obj:
                if user_obj.user_id == cart_data.fk_user_id:
                    session.delete(cart_data)
                    session.commit()
                    content = jsonify({"Success": "cart was deleted"})
                    return content, 200, {'content-type': 'application/json'}
                else:
                    content = jsonify({"Error": "You are not allowed"})
                    return content, 404, {'content-': 'application/json'}
            else:
                content = jsonify({"Error": "User doen'nt exists"})
                return content, 404, {'content-': 'application/json'}

    else:
        content = jsonify({"Error": "Cart  doesn't exists"})
        return content, 404, {'content-': 'application/json'}

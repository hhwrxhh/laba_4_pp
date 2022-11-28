from extensions import app, Session
from flask import request, jsonify
from .models import Cart
from .models import CartHasDosed
from .schema import CartSchema, CartSchemaUpdate
from .schema import CartSchemaGet
from .schema import CartSchemaAdd
from .schema import CartSchemaDosedGet
from ..drug.models import Dosed
from imports import *
from ..user.models import User


@app.route('/cart', methods=['POST'])
@jwt_required()
def cart_post():
    session = Session()
    try:
        cart_data = CartSchema().load(request.json)
        current_identity_email = get_jwt_identity()
        user_data = session.query(User).filter_by(
            email=current_identity_email).first()
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if request.method == 'POST':
        if current_identity_email == user_data.email:
            try:
                request.json['fk_user_id'] = user_data.user_id
                my_post = Cart(**request.json)
                session.add(my_post)
                session.commit()
                return CartSchema().jsonify(my_post)
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
            except IntegrityError as e:
                session.rollback()
                rv = dict({'message': "Dosed don't exist"})
                return rv, 400, {'content-type': 'application/json'}
        else:
            content = jsonify({"Error": "Access is denied"})
            return content, 404, {'content-': 'application/json'}


@app.route('/cart', methods=['GET'])
@jwt_required()
def cart_get():
    session = Session()
    current_identity_email = get_jwt_identity()
    user_data = session.query(User).filter_by(
        email=current_identity_email).first()

    if request.method == 'GET':
        if current_identity_email == user_data.email:
            q = session.query(Cart).filter_by(
                fk_user_id=user_data.user_id).all()

            if not q:
                rv = dict({'message': "Carts are empty"})
                return rv, 400, {'content-type': 'application/json'}
            else:
                return CartSchema(many=True).jsonify(q)
        else:
            content = jsonify({"Error": "Access is denied"})
            return content, 404, {'content-': 'application/json'}


@app.route('/cart/add_new/<cart_id>', methods=['POST', 'GET'])
@jwt_required()
def cart_add_new(cart_id):
    session = Session()

    try:
        current_identity_email = get_jwt_identity()
        user_data = session.query(User).filter_by(
            email=current_identity_email).first()

        cart_request = CartSchemaAdd().load(request.json)
        cart_data = session.query(Cart).filter_by(
            cart_id=cart_id).first()

        dosed_data = session.query(Dosed).filter_by(
            dosed_id=request.json['fk_dosed_id']).first()

    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if current_identity_email == user_data.email:
        if cart_data and dosed_data:
            if user_data.user_id == cart_data.fk_user_id:
                if request.method == 'POST':
                    try:
                        request.json['fk_cart_id'] = cart_id
                        my_post = CartHasDosed(**request.json)
                        session.add(my_post)
                        session.commit()
                        return CartSchema().jsonify(my_post)
                    except ValidationError as e:
                        rv = dict({'message': e.normalized_messages()})
                        return rv, 400, {'content-type': 'application/json'}
                    except IntegrityError as e:
                        session.rollback()
                        errorInfo = e.orig.args
                        rv = dict({'message i': errorInfo[1]})
                        return rv, 400, {'content-type': 'application/json'}
            else:
                content = jsonify({"Error": "You are not allowed to add new to cart"})
                return content, 404, {'content-': 'application/json'}
        else:
            content = jsonify({"Error": "Cart/Dosed doesn't exist"})
            return content, 404, {'content-': 'application/json'}
    else:
        content = jsonify({"Error": "Access is denied"})
        return content, 404, {'content-': 'application/json'}


@app.route('/cart/<id>', methods=['GET'])
@jwt_required()
def cart_g(id):
    session = Session()
    try:
        cart_request = CartSchemaGet().load(request.json)
        cart_data = session.query(Cart).filter_by(
            cart_id=id).first()
        current_identity_email = get_jwt_identity()
        user_data = session.query(User).filter_by(
            email=current_identity_email).first()
        cart_dosed = session.query(CartHasDosed).filter_by(
            fk_cart_id=id).all()
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}
    print(cart_data)
    if cart_data:
        if current_identity_email == user_data.email:
            if user_data.user_id == cart_data.fk_user_id:
                if request.method == 'GET':
                    return CartSchemaDosedGet(many=True).jsonify(cart_dosed)
            else:
                content = jsonify({"Error": "Your don't have this cart"})
                return content, 404, {'content-': 'application/json'}
        else:
            content = jsonify({"Error": "Access is denied"})
            return content, 404, {'content-': 'application/json'}
    else:
        content = jsonify({"Error": "Cart doesn't exists"})
        return content, 404, {'content-': 'application/json'}


@app.route('/cart/<id>',
           methods=['PUT', 'DELETE'])
@jwt_required()
def cart_pd(id):
    session = Session()
    try:
        cart_request = CartSchemaGet().load(request.json)
        cart_data = session.query(Cart).filter_by(
            cart_id=id).first()
        current_identity_email = get_jwt_identity()
        user_data = session.query(User).filter_by(
            email=current_identity_email).first()
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if cart_data:
        if current_identity_email == user_data.email and \
            user_data.user_id == cart_data.fk_user_id:
            if user_data.user_id == cart_data.fk_user_id:
                if request.method == 'PUT':
                    try:
                        cart_request = CartSchemaUpdate().load(request.json)
                    except ValidationError as e:
                        rv = dict({'message': e.normalized_messages()})
                        return rv, 400, {'content-type': 'application/json'}
                    except IntegrityError as e:
                        session.rollback()
                        rv = dict({'message': "Dosed don't exist"})
                        return rv, 400, {'content-type': 'application/json'}

                    try:
                        if 'fk_dosed_id' in request.json:
                            cart_data.fk_dosed_id = cart_request[
                                'fk_dosed_id']
                        else:
                            rv = dict({'message': "Cart is empty"})
                            return rv, 400, {
                                'content-type': 'application/json'}
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

                elif request.method == 'DELETE':
                    if user_data.user_id == cart_data.fk_user_id:
                        cart_dosed = session.query(CartHasDosed).filter_by(
                            fk_cart_id=id).all()
                        for i in cart_dosed:
                            session.delete(i)
                        session.delete(cart_data)
                        session.commit()
                        content = jsonify({"Success": "cart was deleted"})
                        return content, 200, {
                            'content-type': 'application/json'}
                    else:
                        content = jsonify({"Error": "You are not allowed"})
                        return content, 404, {'content-': 'application/json'}
            else:
                content = jsonify({"Error": "Your don't have a cart"})
                return content, 404, {'content-': 'application/json'}
        else:
            content = jsonify({"Error": "Access is denied"})
            return content, 404, {'content-': 'application/json'}
    else:
        content = jsonify({"Error": "Cart doe`nt exist"})
        return content, 404, {'content-': 'application/json'}

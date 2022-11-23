from extensions import app, Session
from flask import request, jsonify
from .models import Category, SubCategory
from .schema import CategorySchema, SubCategorySchema
from .schema import SubCategorySchemaUpdate
from imports import *


@app.route('/category', methods=['POST'])
def category_post():
    session = Session()
    try:
        category_data = CategorySchema().load(request.json)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if request.method == 'POST':
        try:
            my_post = Category(**request.json)
            session.add(my_post)
            session.commit()
            return CategorySchema().jsonify(my_post)
        except ValidationError as e:
            rv = dict({'message': e.normalized_messages()})
            return rv, 400, {'content-type': 'application/json'}
        except OperationalError as e:
            rv = dict({'message': "One of the fields is empty"})
            return rv, 404, {'content-type': 'application/json'}
        except IntegrityError as e:
            session.rollback()
            rv = dict({'message': "Duplicate entry for category"})
            return rv, 400, {'content-type': 'application/json'}


@app.route('/category', methods=['GET'])
def category_get():
    session = Session()
    if request.method == 'GET':
        categories = session.query(Category).all()
        if not categories:
            content = jsonify({"Error": "Database is empty"})
            return content, 404, {'content-type': 'application/json'}
        else:
            return CategorySchema(many=True).jsonify(categories)


@app.route('/category/<id>', methods=['PUT', 'DELETE', 'GET'])
def category_pdg(id):
    session = Session()
    category_data = session.query(Category).get(id)

    if category_data:
        if request.method == 'PUT':
            try:
                category_request = CategorySchema().load(request.json)
                category_data.category_name = category_request['category_name']
                session.commit()
                return CategorySchema().jsonify(category_request)
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
            except IntegrityError as e:
                session.rollback()
                errorInfo = e.orig.args
                rv = dict({'message': errorInfo[1]})
                return rv, 400, {'content-type': 'application/json'}
        elif request.method == 'DELETE':
            session.delete(category_data)
            session.commit()
            content = jsonify({"Success": "Category was deleted"})
            return content, 200, {'content-type': 'application/json'}
        elif request.method == 'GET':
            return CategorySchema().jsonify(category_data)
    else:
        content = jsonify({"Error": "Category doesn't exists"})
        return content, 404, {'content-': 'application/json'}


@app.route('/category/subcategory', methods=['POST'])
def subcategory_post_get():
    session = Session()
    try:
        subcategory_data = SubCategorySchema().load(request.json)
        сat_id = request.json['fk_category_id']
        exist = session.query(Category).get(сat_id)
    except ValidationError as e:
        rv = dict({'message': e.normalized_messages()})
        return rv, 400, {'content-type': 'application/json'}

    if request.method == 'POST':
        if exist:
            try:
                my_post = SubCategory(**request.json)
                session.add(my_post)
                session.commit()
                return SubCategorySchema().jsonify(my_post)
            except OperationalError as e:
                rv = dict({'message': "One of the fields is empty"})
                return rv, 404, {'content-type': 'application/json'}
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
            except IntegrityError as e:
                session.rollback()
                errorInfo = e.orig.args
                rv = dict({'message': errorInfo[1]})
                return rv, 400, {'content-type': 'application/json'}
        else:
            content = jsonify({"Error": "The category doesn't exists"})
            return content, 200, {'content-type': 'application/json'}

    if request.method == 'GET':
        q = session.query(SubCategory).filter(
            SubCategory.fk_category_id == Category.category_id).all()

        if not q:
            content = jsonify({"Error": "Database is empty"})
            return content, 404, {'content-type': 'application/json'}
        return jsonify(SubCategorySchema().dump(q, many=True))


@app.route('/category/subcategory', methods=['GET'])
def subcategory_get():
    session = Session()
    if request.method == 'GET':
        subcategories = session.query(SubCategory).all()
        if not subcategories:
            content = jsonify({"Error": "Database is empty"})
            return content, 404, {'content-type': 'application/json'}
        else:
            return SubCategorySchema(many=True).jsonify(subcategories)


@app.route('/category/subcategory/<id>',
           methods=['PUT', 'DELETE'])
def subcategory_pdg(id):
    session = Session()
    subcategory_data = session.query(SubCategory).filter_by(
        sub_category_id=id).first()

    if subcategory_data:
        if request.method == 'PUT':
            try:
                subcategory_request = SubCategorySchemaUpdate().load(request.json)
                subcategory_data.sub_category_name = subcategory_request[
                    'sub_category_name']
                session.commit()
                return SubCategorySchema().jsonify(subcategory_data)
            except IntegrityError as e:
                session.rollback()
                errorInfo = e.orig.args
                rv = dict({'message': errorInfo[1]})
                return rv, 400, {'content-type': 'application/json'}
            except ValidationError as e:
                rv = dict({'message': e.normalized_messages()})
                return rv, 400, {'content-type': 'application/json'}
        elif request.method == 'DELETE':
            session.delete(subcategory_data)
            session.commit()
            content = jsonify({"Success": "subcategory_data was deleted"})
            return content, 200, {'content-type': 'application/json'}
        elif request.method == 'GET':
            return SubCategorySchema().jsonify(subcategory_data)
    else:
        content = jsonify({"Error": "Subcategory doesn't exists"})
        return content, 404, {'content-': 'application/json'}

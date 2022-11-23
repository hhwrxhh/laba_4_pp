from extensions import db
from imports import *


class Category(db.Model):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                            nullable=False)
    category_name = db.Column(db.String(45), unique=True, nullable=False)

    def __init__(self, category_name):
        self.category_name = category_name


class SubCategory(db.Model):
    __tablename__ = "sub_category"
    sub_category_id = db.Column(Integer, primary_key=True, autoincrement=True,
                                nullable=False)
    sub_category_name = db.Column(db.String(45), nullable=False, unique=True)
    fk_category_id = db.Column(Integer, ForeignKey("category.category_id",
                                                   ondelete='RESTRICT'),
                               primary_key=True, nullable=False)
    category = sqlalchemy.orm.relationship('Category', backref='subcategories')

    def __init(self, sub_category_name):
        self.sub_category_name = sub_category_name

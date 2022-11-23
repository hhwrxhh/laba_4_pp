from extensions import db
from imports import *


class Dosed(db.Model):
    __tablename__ = "dosed"
    dosed_id = db.Column(Integer, primary_key=True, autoincrement=True,
                         nullable=False)
    dosed_name = db.Column(db.String(45), nullable=False)
    dosed_description = db.Column(db.String(45), nullable=False)
    dosed_form = db.Column(
        db.Enum("capsules", "pills", "dragee", "granules", "powders",
                "solutions",
                "infusions",
                "tinctures", "liquid extracts", "emulsions", "mixtures"),
        nullable=False)
    physical_form = db.Column(db.Enum("solid", "liquid"), nullable=False)
    the_number_of_blisters = db.Column(db.SmallInteger, default=null)
    quantity_in_package = db.Column(db.SmallInteger, default=null)
    net_weight = db.Column(Float, nullable=False)
    unit_of_measurement = db.Column(db.Enum("ml", "l", "mg", "gr"),
                                    nullable=False)
    for_a_prescription = db.Column(db.Enum("true", "false"), nullable=False)
    dosed_price = db.Column(Float, nullable=False)
    fk_producer_id = db.Column(Integer, ForeignKey("producer.producer_id",
                                                   ondelete='RESTRICT'),
                               primary_key=True, nullable=False)
    fk_sub_category_id = db.Column(Integer,
                                   ForeignKey("sub_category.sub_category_id",
                                              ondelete='RESTRICT'),
                                   primary_key=True, nullable=False)
    sub_category = sqlalchemy.orm.relationship('SubCategory',
                                               backref='subcategories_')
    producer = sqlalchemy.orm.relationship('Producer', backref='producer')

    def __init(self, dosed_name, dosed_description, dosed_form, physical_form,
               the_number_of_blisters, quantity_in_package, net_weight,
               unit_of_measurement, for_a_prescription, dosed_price
               ):
        self.dosed_name = dosed_name
        self.dosed_description = dosed_description
        self.dosed_form = dosed_form
        self.physical_form = physical_form
        self.the_number_of_blisters = the_number_of_blisters
        self.quantity_in_package = quantity_in_package
        self.net_weight = net_weight
        self.unit_of_measurement = unit_of_measurement
        self.for_a_prescription = for_a_prescription
        self.dosed_price = dosed_price

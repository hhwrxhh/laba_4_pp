from extensions import db
from imports import *

class Producer(db.Model):
    __tablename__ = "producer"
    producer_id = db.Column(Integer, primary_key=True, autoincrement=True,
                            nullable=False)
    producing_company = db.Column(db.String(45), nullable=False)
    producing_country = db.Column(db.String(45), nullable=False)
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt, generate_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
import sqlalchemy.orm
from flask_jwt_extended import JWTManager

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt(app)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

sql_engine = create_engine('mysql://root:lehyfz_[fnf@localhost:3306/laba_6_pp',
                           echo=False)
Session = sessionmaker(bind=sql_engine)



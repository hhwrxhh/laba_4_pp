from flask_bcrypt import Bcrypt, generate_password_hash
from flask_bcrypt import check_password_hash

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from marshmallow.exceptions import ValidationError

from sqlalchemy import exc
from sqlalchemy import *

from marshmallow import validate, fields
from flask_marshmallow import Marshmallow

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


import sqlalchemy.orm
from flask_jwt_extended import get_jwt_identity
from app.user.models import User
from extensions import Session


def admin_required(func):
    def wrapper(*args, **kwargs):
        current_identity_email = get_jwt_identity()
        session = Session()
        user_data = session.query(User).filter_by(
            email=current_identity_email).first()

        if user_data.is_superuser == 'true':
            return func(*args, **kwargs)
        else:
            rv = dict({"error": f"User must be an admin to use {func.__name__}."})
            return rv, 400, {'content-type': 'application/json'}

    wrapper.__name__ = func.__name__
    return wrapper

from flask_jwt_extended import jwt_required, get_jwt
from flask import jsonify , make_response
from functools import wraps

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') != required_role:
                return make_response(jsonify({"msg": "Access forbidden: insufficient permissions"}), 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper
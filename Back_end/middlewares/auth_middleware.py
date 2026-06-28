import jwt
from flask import request, g
from functools import wraps
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        token = request.cookies.get("granja_access_token")

        if not token:
            return {"message": "Token ausente"}, 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            g.user_id = data["user_id"]
            g.user = data

        except jwt.ExpiredSignatureError:
            return {"message": "Token expirado"}, 401

        except jwt.InvalidTokenError as e:
            return {"message": "Token inválido"}, 401

        return f(*args, **kwargs)

    return wrapper
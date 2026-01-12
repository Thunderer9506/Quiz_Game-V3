from functools import wraps
from flask import request, redirect, url_for, flash
import jwt
import os

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("user_id")
        if not token:
            flash("Please login to continue", "error")
            return redirect(url_for("login"))
        
        try:
            user_id = decode_jwt_token(token)
            if not user_id:
                flash("Invalid token", "error")
                return redirect(url_for("login"))
        except Exception as e:
            flash("Invalid token", "error")
            return redirect(url_for("login"))
            
        return f(*args, **kwargs)
    return decorated

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

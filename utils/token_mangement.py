from functools import wraps
from flask import request, redirect, url_for, flash
import jwt
import os
import datetime as dt

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24*7

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("user_id")
        if not token:
            flash("Please login to continue", "error")
            return redirect(url_for("auth.login"))
        
        try:
            user_id = decode_jwt_token(token)
            if not user_id:
                flash("Invalid token", "error")
                return redirect(url_for("auth.login"))
        except Exception as e:
            flash("Invalid token", "error")
            return redirect(url_for("auth.login"))
            
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

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=JWT_EXPIRATION_HOURS),
        'httponly': True,
        'secure': True,
        'samesite': 'Lax',
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
from flask import Blueprint, request, session, render_template, redirect, url_for, flash, make_response
import uuid
from models import db
from schemas.user import User
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import argon2
from utils.token_mangement import token_required, generate_jwt_token
from logger_config import logger

auth_bp = Blueprint('auth', __name__)

ph = argon2.PasswordHasher()

@auth_bp.route("/")
@token_required
def index():
    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        stmt = select(User).where(User.email == email)
        user = db.session.execute(stmt).scalar()
        if user:
            try:
                passwordVerify = ph.verify(user.password_hash,password)
            except:
                passwordVerify = False
            if passwordVerify:
                logger.info(f"User {user.username} logged in successfully")
                session["user_id"] = user.id
                token = generate_jwt_token(user.id)
                response = make_response(redirect(url_for("home")))
                response.set_cookie('user_id', token)
                flash("Login Successful", "success")
                return response
            else:
                flash('Password or Email is Wrong', 'error')
        else:
            flash('Password or Email is Wrong', 'error')
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return redirect(url_for("auth.signup"))
        
        try:
            new_user = User(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                password_hash=str(ph.hash(password))
            )
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"User added successfully of user id: {new_user.id}")
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for("auth.index"))
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"User already exists: {e}")
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(url_for("auth.signup"))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {e}")
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for("auth.signup"))
    return render_template("signup.html")

@auth_bp.get("/logout")
@token_required
def logout():
    session.clear()
    response = make_response(redirect(url_for("auth.index")))
    response.delete_cookie('user_id')
    return response
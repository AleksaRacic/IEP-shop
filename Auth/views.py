import json
import re
from sqlalchemy import and_;
from utils import roleCheck

from flask import Blueprint
from flask import request, Response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt, \
    get_jwt_identity

from models import User, database, UserRole

auth_view = Blueprint('auth_view', __name__)


@auth_view.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    isCustomer = request.json.get("isCustomer", None)

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0
    forenameEmpty = len(forename) == 0
    surnameEmpty = len(surname) == 0
    isCustomerEmpty = isCustomer == None

    if forenameEmpty:
        return Response(json.dumps(
            {'message': 'Field forename is missing.'}
        ), status=400)

    if surnameEmpty:
        return Response(json.dumps(
            {'message': 'Field surname is missing.'}
        ), status=400)

    if emailEmpty:
        return Response(json.dumps(
            {'message': 'Field email is missing.'}
        ), status=400)

    if passwordEmpty:
        return Response(json.dumps({
            'message': 'Field password is missing.'
        }), status=400)

    if isCustomerEmpty:
        return Response(json.dumps({
            'message': 'Field isCustomer is missing.'
        }), status=400)

    email_re = re.compile('([A-Za-z0-9]+[.-?])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    res_email = re.fullmatch(email_re, email)
    if not res_email:
        return Response(json.dumps({
            'message': 'Invalid email.'
        }), status=400)

    match_re = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$")
    res = re.search(match_re, password)


    if not res:
        return Response(json.dumps({
            'message': 'Invalid password.'
        }), status=400)

    testUser = User.query.filter(User.email == email).all()
    if len(testUser) != 0:
        return Response(json.dumps({
            'message': 'Email already exists.'
        }), status=400)

    user = User(email=email, password=password, forename=forename, surname=surname, isCustomer=isCustomer)
    database.session.add(user)
    database.session.commit()
    if isCustomer:
        userRole = UserRole(userId=user.id, roleId=2)
    else:
        userRole = UserRole(userId=user.id, roleId=3)

    database.session.add(userRole)
    database.session.commit()

    return Response(status=200)


@auth_view.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0

    if emailEmpty:
        return Response(json.dumps({
            'message': 'Field email is missing.'
        }), status=400)

    if passwordEmpty:
        return Response(json.dumps({
            'message': 'Field password is missing.'
        }), status=400)

    email_re = re.compile('([A-Za-z0-9]+[.-?])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    res_email = re.fullmatch(email_re, email)
    if not res_email:
        return Response(json.dumps({
            'message': 'Invalid email.'
        }), status=400)

    user = User.query.filter(and_(User.email == email, User.password == password)).first()

    if (not user):
        return Response(json.dumps({
            'message': 'Invalid credentials.'
        }), status=400)

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        'email': user.email,
        'isCustomer': user.isCustomer,
        "roles": [str(role) for role in user.roles]
    }

    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims)

    return Response(json.dumps({
        'accessToken': accessToken,
        'refreshToken': refreshToken
    }), status=200)

@auth_view.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # moguce da ce trebati custom wrapper jer treba u specificnom formatu da se vraca response
def refresh():
    identity = get_jwt_identity()
    refreshClaims = get_jwt()

    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        'email': refreshClaims["email"],
        'isCustomer': refreshClaims["isCustomer"],
        "roles": refreshClaims["roles"]
    }

    return jsonify(accessToken=create_access_token(identity=identity, additional_claims=additionalClaims)), 200


@auth_view.route("/delete", methods=["POST"])
@roleCheck(role="Admin")
def delete():
    email = request.json.get("email", "")
    emailEmpty = len(email) == 0

    if emailEmpty:
        return Response(json.dumps({
            'message': 'Field email is missing.'
        }), status=400)

    email_re = re.compile('([A-Za-z0-9]+[.-?])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    res_email = re.fullmatch(email_re, email)
    if not res_email:
        return Response(json.dumps({
            'message': 'Invalid email.'
        }), status=400)

    user = User.query.filter(User.email == email).first()
    if not user:
        return Response(json.dumps({
            'message': 'Unknown user.'
        }), status=400)

    database.session.delete(user)
    database.session.commit()
    return Response(status=200)


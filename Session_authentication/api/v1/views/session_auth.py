#!/usr/bin/env python3
"""A Flask view module 
"""
from api.v1.views import app_views
from flask import abort, request, jsonify


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Login function
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == "":
        return jsonify("error": "email missing"), 400

    if not password or password == "":
        return jsonify("error": "password missing"), 400
 
    from models.user import User
    try:
        users = User.search({"email": user_email})
    except Exception:
        return None

    if  not users:
        return jsonify("error": "no user found for this email"), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify("error": "wrong password"), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
        

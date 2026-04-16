#!/usr/bin/env python3
"""Flask module
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """Home route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """POST /sessions
    Return:
    - 401, if login info is incorrect
    - JSON payload of the response
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response_payload = jsonify({"email": email, "message": "logged in"})
    response = make_response(response_payload)
    response.set_cookie("session_id", session_id)
    return response


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Users route
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({
                "email": email,
                "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """GET /profile
    Return:
    - 200, if user exists
    - 403, if session_id is invalid or user doesn't exist
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password():
    """POST /reset_password
    Return:
    - 403, if email is not registered
    - 200, if email is registered
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /logout
    Return:
    - 403, if user does not exist
    - redirect to GET /
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

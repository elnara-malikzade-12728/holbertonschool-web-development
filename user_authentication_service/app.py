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


@app.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /logout
    Return:
    - 403, if user does not exist
    - redirect to GET /
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)

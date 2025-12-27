from flask import Blueprint, jsonify

api_bp = Blueprint("api_bp", __name__)
@api_bp.route("/test")
def test():
    return jsonify('Hello world')

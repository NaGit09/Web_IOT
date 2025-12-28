from flask import Blueprint, jsonify, request
from app.services.api import API

api_bp = Blueprint("api_bp", __name__)


@api_bp.route("/test")
def test():
    return jsonify("Hello world")


@api_bp.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    username = body.get("username")
    password = body.get("password")

    return jsonify(API().login(username, password))


@api_bp.route("/relay_state")
def relay_state():
    return jsonify(API().get_relay_state())


@api_bp.route("/relay_state_db")
def relay_state_db():
    return jsonify(API().get_relay_state_db())


@api_bp.route("/update_relay_state_db", methods=["POST"])
def update_relay_state_db():
    body = request.get_json()
    relay_id = body.get("relay_id")
    state = body.get("state")
    return jsonify(API().update_relay_state_db(relay_id, state))


@api_bp.route("/update_relay_mode_db", methods=["POST"])
def update_relay_mode_db():
    body = request.get_json()
    relay_id = body.get("relay_id")
    mode = body.get("mode")
    return jsonify(API().update_relay_mode_db(relay_id, mode))


@api_bp.route("/latest_luuluong_1_2_and_total")
def latest_luuluong_1_2_and_total():
    return jsonify(API().get_latest_luuluong_1_2_and_total())


@api_bp.route("/latest_apxuat")
def latest_apxuat():
    return jsonify(API().get_latest_apxuat())


@api_bp.route("/latest_ec")
def latest_ec():
    return jsonify(API().get_latest_ec())


@api_bp.route("/latest_ph")
def latest_ph():
    return jsonify(API().get_latest_ph())


@api_bp.route("/history_data")
def history_data():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    return jsonify(API().get_history_data(start_time, end_time))


@api_bp.route("/data_luu_luong")
def data_luu_luong():
    id = request.args.get("id")
    return jsonify(API().get_data_luu_luong(id))


@api_bp.route("/data_apxuat")
def data_apxuat():
    return jsonify(API().get_data_apxuat())


@api_bp.route("/data_ec")
def data_ec():
    return jsonify(API().get_data_ec())


@api_bp.route("/data_ph")
def data_ph():
    return jsonify(API().get_data_ph())

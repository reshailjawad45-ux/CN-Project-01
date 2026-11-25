
from flask import Blueprint, request, jsonify, g
from app import db
from models import Record
from utils.auth_guard import login_required
from utils.crypto import encrypt_phone, decrypt_phone

records_bp = Blueprint("records", __name__)
@records_bp.route("", methods=["POST"])
@login_required
def create_record():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid JSON data"
        }), 400
    name = data.get("name")
    course = data.get("course")
    phone = data.get("phone")
    if not all(isinstance(x, str) for x in [name, course, phone]):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Name, course and phone are required"
        }), 400
    name = name.strip()
    course = course.strip()
    phone = phone.strip()
    if not name or not course or not phone:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Fields cannot be empty"
        }), 400
    if len(name) > 100 or len(course) > 100 or len(phone) > 30:
        return jsonify({
            "success": False,
            "data": None,
            "error": "One or more fields are too long"
        }), 400

    record = Record(
        name=name,course=course,phone=encrypt_phone(phone),owner_id=g.current_user.id)

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": {
            "id": record.id,
            "name": record.name,
            "course": record.course,
            "phone": phone,
            "owner_id": record.owner_id
        },
        "error": None
    }), 201


@records_bp.route("", methods=["GET"])
@login_required
def get_records():
    user_id=g.current_user.id
    records=Record.query.filter_by(
        owner_id=user_id
    ).order_by(Record.id.desc()).all()


    result=[]

    for record in records:
        result.append({
            "id": record.id,
            "name": record.name,
            "course": record.course,
            "phone": decrypt_phone(record.phone),
            "owner_id": record.owner_id
        })

    return jsonify({
        "success": True,
        "data": result,
        "error": None
    }), 200


@records_bp.route("/<int:record_id>", methods=["PUT"])
@login_required
def update_record(record_id):

    record = Record.query.filter_by(
        id=record_id,
        owner_id=g.current_user.id
    ).first()

    if record is None:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Record not found"
        }), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Invalid JSON data"
        }), 400

    name = data.get("name")
    course = data.get("course")
    phone = data.get("phone")

    if not all(isinstance(x, str) for x in [name, course, phone]):
        return jsonify({
            "success": False,
            "data": None,
            "error": "All fields are required"
        }), 400

    name = name.strip()
    course = course.strip()
    phone = phone.strip()

    if not name or not course or not phone:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Fields cannot be empty"
        }), 400

    if len(name) > 100 or len(course) > 100 or len(phone) > 30:
        return jsonify({
            "success": False,
            "data": None,
            "error": "One or more fields are too long"
        }), 400

    record.name = name
    record.course = course
    record.phone = encrypt_phone(phone)

    db.session.commit()

    return jsonify({
        "success": True,
        "data": {
            "id": record.id,
            "name": record.name,
            "course": record.course,
            "phone": phone,
            "owner_id": record.owner_id
        },
        "error": None
    }), 200


@records_bp.route("/<int:record_id>", methods=["DELETE"])
@login_required
def delete_record(record_id):
    record=Record.query.filter_by(
        id=record_id,
        owner_id=g.current_user.id
    ).first()

    if record is None:
        return jsonify({
            "success": False,
            "data": None,
            "error": "Record not found"
        }),404

    db.session.delete(record)
    db.session.commit()

    return jsonify({
         "success": True,
        "data": {
            "message": "Record deleted successfully"
        },
        "error": None
    }),200

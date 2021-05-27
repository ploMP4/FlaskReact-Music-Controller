from flask import Blueprint, json, request, jsonify, session
from .models import Room
from .utils import generate_session_key
from . import db

views = Blueprint('views', __name__)


@views.route('/home')
def home():
    return jsonify({"data": "Test"})


@views.route('/create-room', methods=['POST'])
def create_room():
    if not 'key' in session:
        session['key'] = generate_session_key()

    data = json.loads(request.data)
    guest_can_pause = data['guest_can_pause']
    votes_to_skip = data['votes_to_skip']
    host = session['key']
    room = Room.query.filter_by(host=host).first()
    if room:
        room.guest_can_pause = guest_can_pause
        room.votes_to_skip = votes_to_skip
        db.session.commit()
        session['room_code'] = room.code
    else:
        room = Room(host=host, guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip)
        db.session.add(room)
        db.session.commit()
        session['room_code'] = room.code
        return jsonify(room.as_dict()), 201

    return jsonify({"Bad Request": "Invalid data..."}), 400


@views.route('/leave-room', methods=['POST'])
def leave_room():
    if 'room_code' in session:
        session.pop('room_code')
        
        host_id = session['key']
        room = Room.query.filter_by(host=host_id).first()
        if room:
            db.session.delete(room)
            db.session.commit()

    return jsonify({"Message": "Success"}), 200


@views.route('/join-room', methods=['POST'])
def join_room():
    if not 'key' in session:
        session['key'] = generate_session_key()

    data = json.loads(request.data)
    code = data['code']
    if code != None:
        room_result = Room.query.filter_by(code=code).first()
        if room_result:
            session['room_code'] = code
            return jsonify({'Message': 'Room Joined'}), 200

    return jsonify({'Bad Request': 'Invalid Data'}), 400


@views.route('/get-room', methods=['GET'])
def get_room():
    code = request.args['code']
    room = Room.query.filter_by(code=code).first()
    if room:
        data = room.as_dict()
        data['is_host'] = session['key'] == room.host
        return jsonify(data), 200

    return jsonify({'Bad Request': 'Invalid Data'}), 400


@views.route('/user-in-room', methods=['GET'])
def user_in_room():
    if not 'key' in session:
        session['key'] = generate_session_key()

    if 'room_code' in session:    
        data = {
            'code': session['room_code']
        }

        return jsonify(data), 200

    return jsonify({'Bad Request': 'Invalid Data'}), 404


@views.route('/update-room', methods=['PATCH'])
def update_room():
    if not 'key' in session:
        session['key'] = generate_session_key()

    data = json.loads(request.data)
    guest_can_pause = data['guest_can_pause']
    votes_to_skip = data['votes_to_skip']
    code = data['code']

    room = Room.query.filter_by(code=code).first()
    if room:
        user_id = session['key']
        if room.host == user_id:
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            db.session.commit()
            return jsonify(room.as_dict()), 200

    return jsonify({'Bad Request': 'Invalid Data'}), 400

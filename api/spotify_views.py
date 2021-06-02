from flask import Blueprint, jsonify, request, session, redirect
from requests import Request, post
from dotenv import load_dotenv
from .utils import *
from .models import Room, Vote
import os

spotify = Blueprint('spotify', __name__)

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

SPOTIFY_URL = 'https://accounts.spotify.com'

@spotify.route('/get-auth-url', methods=['GET'])
def auth_url():
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

    url = Request('GET', f'{SPOTIFY_URL}/authorize', params={
        'scope': scope,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID
    }).prepare().url

    return jsonify({'url': url}), 200


@spotify.route('/redirect')
def spotify_callback():
    code = request.args['code']

    response = post(f'{SPOTIFY_URL}/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    if not 'key' in session:
        session['key'] = generate_session_key()

    update_or_create_user_tokens(session['key'], access_token, token_type, expires_in, refresh_token)

    return redirect('http://127.0.0.1:3000')


@spotify.route('/is-authenticated', methods=['GET'])
def is_authenticated():
    is_authenticated = is_spotify_authenticated(session['key'])
    return jsonify({'status': is_authenticated}), 200
    

@spotify.route('/current-song', methods=['GET'])
def get_current_song():
    room_code = session['room_code']
    room = Room.query.filter_by(code=room_code).first()

    if not room:    
        return jsonify({}), 404

    host = room.host
    endpoint = "/player/currently-playing"
    response = execute_spotify_api_request(host, endpoint)

    if 'error' in response or 'item' not in response:
        return jsonify({}), 204

    item = response.get('item')
    duration = item.get('duration_ms')
    progress = response.get('progress_ms')
    album_cover = item.get('album').get('images')[0].get('url')
    is_playing = response.get('is_playing')
    song_id = item.get('id')

    artist_string = ""

    for i, artist in enumerate(item.get('artists')):
        if i > 0:
            artist_string += ", "
        name = artist.get('name')
        artist_string += name

    votes = len(Vote.query.filter_by(room=room, song_id=song_id).all())

    song = {
        'title': item.get('name'),
        'artist': artist_string,
        'duration': duration,
        'time': progress,
        'image_url': album_cover,
        'is_playing': is_playing,
        'votes': votes,
        'votes_required': room.votes_to_skip,
        'id': song_id
    }

    update_room_song(room, song_id)

    return jsonify(song), 200


@spotify.route('/play', methods=['PUT'])
def play():
    room_code = session['room_code']
    room = Room.query.filter_by(code=room_code).first()
    if session['key'] == room.host or room.guest_can_pause:
        play_song(room.host)
        return jsonify({}), 204

    return jsonify({}), 403


@spotify.route('/pause', methods=['PUT'])
def pause():
    room_code = session['room_code']
    room = Room.query.filter_by(code=room_code).first()
    if session['key'] == room.host or room.guest_can_pause:
        pause_song(room.host)
        return jsonify({}), 204

    return jsonify({}), 403


@spotify.route('/skip', methods=['POST'])
def skip():
    room_code = session['room_code']
    room = Room.query.filter_by(code=room_code).first()
    votes = Vote.query.filter_by(room=room, song_id=room.current_song).all()
    votes_needed = room.votes_to_skip
    
    if session['key'] == room.host or len(votes) + 1 >= votes_needed:
        for vote in votes:
            db.session.delete(vote)
        db.session.commit()
        skip_song(room.host)
    else:
        vote = Vote(user=session['key'], song_id=room.current_song, room=room)
        db.session.add(vote)
        db.session.commit()

    return jsonify({}), 204
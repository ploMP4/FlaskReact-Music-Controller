from flask.json import jsonify
from .models import SpotifyToken, Vote, Room
from datetime import timedelta, datetime
from dotenv import load_dotenv
from requests import post, put, get
from . import db
import string
import secrets
import os
import random

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

SPOTIFY_URL = 'https://accounts.spotify.com'
BASE_URL = 'https://api.spotify.com/v1/me'

def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.query.filter_by(code=code).count() == 0:
            break
    
    return code


def generate_session_key():
    alphabet = string.ascii_letters + string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(8))

    return code


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.query.filter_by(user=session_id).first()
    if user_tokens:
        return user_tokens
    else:
        return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = datetime.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        db.session.commit()
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        db.session.add(tokens)
        db.session.commit()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= datetime.now():
            refresh_spotify_token(session_id)

        return True

    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post(f'{SPOTIFY_URL}/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + tokens.access_token
    }

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)
    
    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return jsonify({'Error': 'Issue with request'}), 400
    

def play_song(session_id):
    execute_spotify_api_request(session_id, "/player/play", put_=True)


def pause_song(session_id):
    execute_spotify_api_request(session_id, "/player/pause", put_=True)


def skip_song(session_id):
    execute_spotify_api_request(session_id, "/player/next", post_=True)


def update_room_song(room, song_id):
    current_song = room.current_song

    if current_song != song_id:
        room.current_song = song_id
        db.session.commit()
        votes = Vote.query.filter_by(room=room, song_id=song_id).all()
        for vote in votes:
            db.session.delete(vote)
        db.session.commit()

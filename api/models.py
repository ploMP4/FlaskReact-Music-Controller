from sqlalchemy.sql.expression import true
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import orm
import datetime
import random
import string


def generate_unique_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.query.filter_by(code=code).count() == 0:
            break
    
    return code


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), default=generate_unique_code)
    host = db.Column(db.String(50), unique=True)
    guest_can_pause = db.Column(db.Boolean, nullable=False, default=False)
    votes_to_skip = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    current_song = db.Column(db.String(50), nullable=True)
    votes = db.relationship('Vote')

    def as_dict(self):
        # Returns full representation of model.
        columns = orm.class_mapper(self.__class__).mapped_table.c
        return {
            col.name: getattr(self, col.name)
                for col in columns
        }


class SpotifyToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    refresh_token = db.Column(db.String(150))
    access_token = db.Column(db.String(150))
    expires_in = db.Column(db.DateTime)
    token_type = db.Column(db.String(50))


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    song_id = db.Column(db.String(50))
    room = db.Column(db.Integer, db.ForeignKey('room.id'))
import sqlite3
from db import db

class RawdataModel(db.Model):
    __tablename__ = 'rawdatas'

    id = db.Column(db.Integer, primary_key=True)
    ax = db.Column(db.Float(precision=2))
    ay = db.Column(db.Float(precision=2))
    az = db.Column(db.Float(precision=2))
    pitch = db.Column(db.Float(precision=2))
    roll = db.Column(db.Float(precision=2))
    heading = db.Column(db.Float(precision=2))
    waveparam_id = db.Column(db.Integer, db.ForeignKey('waveparams.id'))
    waveparam =db.relationship('WaveparamModel')

    def __init__(self, ax, ay, az, pitch, roll, heading, waveparam_id):
        self.ax = ax
        self.ay = ay
        self.az = az
        self.pitch = pitch
        self.roll = roll
        self.heading = heading
        self.waveparam_id = waveparam_id

    def json(self):
        return {'ax': self.ax, 'ay': self.ay, 'az': self.az,
                'pitch': self.pitch, 'roll': self.roll,
                'heading': self.heading, 'waveparam_id': self.waveparam_id}

    @classmethod
    def find_by_waveparam_id(cls, waveparam_id):
        return cls.query.filter_by(waveparam_id=waveparam_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

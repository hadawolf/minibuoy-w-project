import sqlite3
from db import db

class WaveparamModel(db.Model):
    __tablename__ = 'waveparams'

    id = db.Column(db.Integer, primary_key=True)
    timeline = db.Column(db.Integer)
    hs = db.Column(db.Float(precision=2))
    ts = db.Column(db.Float(precision=2))
    tp = db.Column(db.Float(precision=2))
    wdir = db.Column(db.Float(precision=2))

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event = db.relationship('EventModel')
    rawdatas = db.relationship('RawdataModel',lazy='dynamic')


    def __init__(self, timeline, hs, ts, tp, wdir, event_id):
        self.timeline = timeline
        self.hs = hs
        self.ts = ts
        self.tp = tp
        self.wdir = wdir
        self.event_id = event_id

    def json(self):
        return {'timeline': self.timeline, 'hs': self.hs, 'ts': self.ts,
                'tp': self.tp, 'wdir': self.wdir, 'event_id': self.event_id,
                'rawdata': [rawdata.json() for rawdata in self.rawdatas.all()]}

    @classmethod
    def find_by_timeline(cls, timeline1, timeline2):
        return cls.query.filter(cls.timeline.between(timeline1,timeline2)).all()

    @classmethod
    def find_by_timeline_event(cls, timeline1, timeline2, event_id):
        return cls.query.filter(cls.timeline.between(timeline1,timeline2)).filter_by(event_id=event_id).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

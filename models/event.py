import sqlite3
from db import db

class EventModel(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    timeline = db.Column(db.Integer)
    srate = db.Column(db.Float(precision=2))
    scount = db.Column(db.Float(precision=2))
    ointerval = db.Column(db.Float(precision=2))
    commstatus = db.Column(db.String(4))

    waveparams = db.relationship('WaveparamModel',lazy='dynamic')
    #rawdatas = db.relationship('RawdataModel',lazy='dynamic')

    def __init__(self, name, timeline, srate, scount, ointerval, commstatus):
        self.name = name
        self.timeline = timeline
        self.srate = srate
        self.scount = scount
        self.ointerval = ointerval
        self.commstatus = commstatus

    def json(self):
        return {'name': self.name, 'datetime': self.timeline,
                'samplingrate': self.srate, 'samplingnum': self.scount,
                'obsinterval': self.ointerval, 'IridiumOnOff': self.commstatus,
                'waveparams': [waveparam.json() for waveparam in self.waveparams.all()]}
                #'rawdata': [rawdata.json() for rawdata in self.rawdatas.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_timeline(cls, timeline1, timeline2):
        return cls.query.filter(cls.timeline.between(timeline1,timeline2)).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

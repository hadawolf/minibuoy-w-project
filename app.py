from flask import Flask, request
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.waveparam import Waveparam, WaveparamList
from resources.event import Event, EventList
from resources.rawdata import Rawdata

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wolf'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Event, '/event/<string:name>')
api.add_resource(Waveparam, '/waveparam')
api.add_resource(Rawdata, '/rawdata')
api.add_resource(WaveparamList, '/waveparams')
api.add_resource(EventList, '/events')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True

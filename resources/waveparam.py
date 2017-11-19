from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.waveparam import WaveparamModel

class Waveparam(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('timeline1',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('timeline2',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('event_id',
        type=str,
        required=True,
        help="Event_id cannot be left blank!"
    )

    parser1 = reqparse.RequestParser()
    parser1.add_argument('timeline',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('hs',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('ts',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('tp',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('wdir',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('event_id',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self):
        args = Waveparam.parser.parse_args()
        if safe_str_cmp(args['event_id'], "events"):
            waveparam = WaveparamModel.find_by_timeline(args['timeline1'], args['timeline2'])
        else:
            waveparam = WaveparamModel.find_by_timeline_event(**args)
        if waveparam:
            return {'waveparams': [x.json() for x in waveparam]}
        return {'message': 'Data not found'}, 404

    @jwt_required()
    def delete(self):
        args = Waveparam.parser.parse_args()
        if safe_str_cmp(args['event_id'], "events"):
            waveparam = WaveparamModel.find_by_timeline(args['timeline1'], args['timeline2'])
        else:
            waveparam = WaveparamModel.find_by_timeline_event(**args)
        if waveparam:
            [x.delete_from_db() for x in waveparam]

        return {'message': 'Waveparam deleted'}

    @jwt_required()
    def post(self):
        args = Waveparam.parser1.parse_args()
        if WaveparamModel.find_by_timeline(args['timeline'], args['timeline']):
            return {'message': "A event with timeline '{}' already exists.".format(args['timeline'])}, 400

        waveparam = WaveparamModel(**args)
        try:
            waveparam.save_to_db()
        except:
            return {'message': 'An error occurred while creating the waveparam.'}, 500

        return waveparam.json(), 201


class WaveparamList(Resource):

    def get(self):
        return {'waveparams': [x.json() for x in WaveparamModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

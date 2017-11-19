from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from models.event import EventModel

class Event(Resource):

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

    parser1 = reqparse.RequestParser()
    parser1.add_argument('timeline',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('srate',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('scount',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('ointerval',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser1.add_argument('commstatus',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, name):
        args = Event.parser.parse_args()
        if safe_str_cmp(name, "events"):
            event = EventModel.find_by_timeline(**args)
            if event:
                return {'events': [x.json() for x in event]}
        else:
            event = EventModel.find_by_name(name)
            if event:
                return {'events': event.json()}
            #return {'events': [x.json() for x in event]}
        return {'message': 'Event not found'}, 404

    def delete(self, name):
        if safe_str_cmp(name, "events"):
            [event.delete_from_db() for event in EventModel.query.all()]
        else:
            event = EventModel.find_by_name(name)
            if event:
                event.delete_from_db()

        return {'message': 'Event deleted'}

    def post(self, name):
        args = Event.parser1.parse_args()
        if EventModel.find_by_name(name):
            return {'message': "A event with name '{}' already exists.".format(name)}, 400

        event = EventModel(name, **args)
        try:
            event.save_to_db()
        except:
            return {'message': 'An error occurred while creating the event.'}, 500

        return event.json(), 201


class EventList(Resource):
    def get(self):
        return {'events': [event.json() for event in EventModel.query.all()]}

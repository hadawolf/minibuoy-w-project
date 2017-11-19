from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.rawdata import RawdataModel

class Rawdata(Resource):

    parser1 = reqparse.RequestParser()
    parser1.add_argument('waveparam_id',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser = reqparse.RequestParser()
    parser.add_argument('waveparam_id',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('ax',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('ay',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('az',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('pitch',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('roll',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('heading',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # @jwt_required()
    # def get(self, name):
    #     item = ItemModel.find_by_name(name)
    #     if item:
    #         return item.json()
    #     return {'message': 'Item not found'}, 404
    @jwt_required()
    def post(self):
        args = Rawdata.parser.parse_args()
        if RawdataModel.find_by_waveparam_id(args['waveparam_id']):
            return {'message': "Rawdata with id '{}' already exists.".format(args['waveparam_id'])}, 400

        rawdata = RawdataModel(**args)

        try:
            rawdata.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return rawdata.json(), 201

    @jwt_required()
    def delete(self):
        args = Rawdata.parser1.parse_args()
        rawdata =RawdataModel.find_by_waveparam_id(args['waveparam_id'])
        if rawdata:
            [data.delete_from_db() for data in rawdata]

        return {'message': 'Rawdata deleted'}

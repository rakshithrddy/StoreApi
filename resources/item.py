from flask_jwt import jwt_required
from flask_restful import reqparse, Resource
from models.item import ItemModel

path_to_db = r'C:\Users\raksh\PycharmProjects\Flask project\data.db'


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank!')

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='Every item needs a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name=name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name=name):
            return {'message': 'item exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name=name, **data)
        try:
            item.save_to_db()
        except Exception as e:
            print(e)
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name=name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

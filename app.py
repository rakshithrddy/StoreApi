from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from security import identity, authenticate
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'fdshfadsfbadsf'
api = Api(app=app)

jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app=app)
    app.run(port=8000, debug=True)

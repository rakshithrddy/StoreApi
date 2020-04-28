from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'fdshfadsfbadsf'  # app.config['JWT_SECRET_KEY']
api = Api(app=app)

jwt = JWTManager(app=app)


@jwt.user_claims_loader
def add_clams_to_jwt(identity):
    if identity == 1:  # read from database
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': "the token has expired",
        'error': 'token_expired'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': "Signature verification failed",
        'error': 'invalid token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': "Request does not contain an access token",
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': "The token is not fresh",
        'error': 'Fresh token required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': "The token has been revoked",
        'error': 'token revoked'
    }), 401


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db


    @app.before_first_request
    def create_tables():
        db.create_all()


    db.init_app(app=app)
    app.run(port=8000, debug=True)

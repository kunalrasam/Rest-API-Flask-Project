from flask import Flask, jsonify
from flask_smorest import Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST
from db import db
from flask_migrate import Migrate
import models
import secrets
import os
from flask_jwt_extended import JWTManager

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate=Migrate(app,db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"]="kunal"
    jwt=JWTManager(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header,jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "The token is not fresh", "error": "fresh token required"}), 401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header,jwt_payload):
        return (
            jsonify({"message":"The token has expired","error":"token_expired"}),401,
        )

    @jwt.invalid_token_loader
    def expired_token_callback(error):
        return (
            jsonify({"message": "Signature verification failed", "error": "invalid token"}), 401,
        )


    @jwt.unauthorized_loader
    def expired_token_callback(error):
        return (
            jsonify({"description": "request does not contain an access token", "error": "authorization required"}), 401,
        )

   # with app.app_context():
    #    db.create_all()


    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app

    """"
    #retriving all stores
    @app.get("/store")
    def get_store():
        return {"stores":list(stores.values())}
    
    #retriving store with specific store name
    @app.get("/store/<string:store_id>")
    def get_specific_store(store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message= "store not found")
    
    #adding store
    @app.post("/store")
    def create_store():
        store_data=request.get_json()
        if "name" not in store_data:
            abort(404, message="bad request, ensure name is added in store data")
    
        for store in stores.values():
            if store_data["name"]==store["name"]:
                abort(404, message="store already exist")
        store_id=uuid.uuid4().hex
        store={**store_data,"id":store_id}
        stores[store_id]=store
        return store,201
    
    #deleting specific store
    @app.delete("/store/<string:store_id>")
    def del_store(store_id):
        try:
            del stores[store_id]
            return {"message":"store deleted"}
        except KeyError:
            abort(404 ,message="store cannot be deleted")
    
    #************************************************************************************************
    
    #retriving all items
    
    @app.get("/item")
    def get_all_items():
        return "hello"
        return {"items":list(items.values())}
    
    #retriving specific item
    @app.get("/item/<string:item_id>")
    def get_item(item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message= "item not found")
    
    
    #adding items in specific store
    @app.post("/item")
    def create_item():
        item_data=request.get_json()
        if (
            "price" not in item_data or
            "store_id" not in item_data or
            "name" not in item_data
        ):
            abort(404, message= "bad request , ensure price store id name is mention in json")
    
        #checking if item is already available in items dic
        for item in items.values():
            if item_data["name"]==item["name"] and item_data["store_id"]==item["store_id"]:
                abort(404 ,message="item already exist")
    
        if item_data["store_id"] not in stores:
            abort(404, message= "store not found")
        item_id=uuid.uuid4().hex
        item={**item_data,"id":item_id}
        items[item_id]=item
        return item,201
    
    
    #update items
    @app.put("/item/<string:item_id>")
    def update_item(item_id):
        item_data=request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(404,message="please mention price name in req")
    
        try:
            item=items[item_id]
            item |= item_data
            return item,{"message":"item found"}
        except KeyError:
            abort(404,message="item not found")
    
    #deleting specific item
    @app.delete("/item/<string:item_id>")
    def del_item(item_id):
        try:
            del items[item_id]
            return {"message":"item deleted"}
        except KeyError:
            abort(404, message= "item not found")
    
    """




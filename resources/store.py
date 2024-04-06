import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from schemas import StoreSchema
from models import StoreModel


blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    #get perticular store
    @blp.response(200, StoreSchema)
    def get(self,store_id):

        """try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")
        """
        store = StoreModel.query.get_or_404(store_id)
        return store

    #delete store
    def delete(self,store_id):
        """try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")"""
        store=StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    #get all stores
    @blp.response(201, StoreSchema(many=True))
    def get(self):
        #return {"stores": list(stores.values())} -> this was before adding marshmallow response , as we only need to return dict , list will be created by storeschema
        return StoreModel.query.all()

    #add store
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self,store_data):

        #below manual validation required before marshmallow
        #store_data = request.get_json()
        """if "name" not in store_data:
            abort(
                400,
                message="Bad request. Ensure 'name' is included in the JSON payload.",
            )
            """

        #as we are checking this that store is present already , we are checking this in models.store py we can get rid of this

        """for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        """

        # this is sql code to create item

        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()

        except IntegrityError:
            abort(
                400,
                message="a store with name already exist"
            )
        except SQLAlchemyError:
            abort(500, message="error occured while inserting store")

        return store
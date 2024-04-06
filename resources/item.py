
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema,ItemUpdateSchema,PlainItemSchema,StoreSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # returning perticular item
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self, item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item


    #deleting items
    @jwt_required()
    def delete(self, item_id):

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "item deleted"}

        #try:
        #    del items[item_id]
        #    return {"message": "Item deleted."}
        #except KeyError:
        #    abort(404, message="Item not found.")"""

    # update items
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self,item_data,item_id):
        # ->below manual validation was required before marshmallow added
        #item_data = request.get_json()

        """if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
            )
        """
        """try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
             abort(404, message="Item not found.")"""


        item = ItemModel.query.get(item_id)
        if item:
            item.price=item_data["price"]
            item.name=item_data["name"]
        else:
            item=ItemModel(id=item_id,**item_data)
        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemList(MethodView):
    #returning all items

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        #return {"items": list(items.values())} -> this was code before response , ItemSchema now includes list to response and sent to server
        return ItemModel.query.all()



    #adding items to store
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        #item_data = request.get_json() - > this was used before itemschema used
        # but as schema is used it only received data from json payload and sends to function


        #as we are checking this that item is present already , we are checking this in models.item py we can get rid of this
        """for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        """
        #this is sql code to create item

        item=ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="error occured while inserting item ")

        return item
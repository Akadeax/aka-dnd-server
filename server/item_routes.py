from .index import db

from bson import ObjectId
from flask import Blueprint, jsonify, request

from server.models.item import ItemSchema

item_api = Blueprint("item_api", __name__)

@item_api.route('/item', methods=['GET'])
def get_items():
    collection_name: str = request.args.get('collection')
    collection = db.get_collection(collection_name)
    if collection is None:
        return "collection invalid", 400

    items_list = list(collection.find())

    validation_errors = ItemSchema().validate(items_list, many=True)

    if len(validation_errors) > 0:
        return jsonify({"errors": validation_errors}), 400

    items_dic = ItemSchema().dump(items_list, many=True)
    return jsonify(items_dic), 200


@item_api.route('/item', methods=['POST'])
def add_item():
    collection_name: str = request.args.get('collection')
    collection = db.get_collection(collection_name)
    if collection is None:
        return "collection invalid", 400

    try:
        item_json = request.get_json()

        validation_errors = ItemSchema().validate(item_json)

        if len(validation_errors) > 0:
            return jsonify({"errors": validation_errors}), 400

        collection.insert_one(item_json)
        return "item added", 201
    
    except Exception as e:
        return str(e), 400


@item_api.route('/item', methods=['DELETE'])
def delete_item():
    collection_name: str = request.args.get('collection')
    collection = db.get_collection(collection_name)
    if collection is None:
        return "collection invalid", 400

    try:
        id_to_delete = ObjectId(request.args.get('id'))
    except Exception as e:
        return str(e), 400

    result = collection.delete_one({"_id": id_to_delete})

    if result.deleted_count != 1:
        return "item with ID not found", 404
    
    return "item deleted", 200


@item_api.route('/item', methods=['PATCH'])
def update_item():
    collection_name: str = request.args.get('collection')
    collection = db.get_collection(collection_name)
    if collection is None:
        return "collection invalid", 400
    
    try:
        id_to_update = ObjectId(request.args.get('id'))
    except Exception as e:
        return str(e), 400
    
    updated_data = request.get_json()

    if not updated_data:
        return "No data provided", 400
    
    if "_id" in updated_data:
        del updated_data["_id"] # remove so we can't alter id

    validation_errors = ItemSchema().validate(updated_data, partial=True)
    if len(validation_errors) > 0:
        return jsonify({"errors": validation_errors}), 400

    result = collection.update_one(
        {"_id": id_to_update},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        return "item with ID not found", 404
    
    return "item updated", 200
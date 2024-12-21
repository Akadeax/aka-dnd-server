from .index import db

from flask import Blueprint, request

from server.models.user import User, UserSchema

users_collection = db["users"]
user_api = Blueprint("user_api", __name__)

@user_api.route('/users', methods=['GET'])
def get_user():
    name = request.args.get('name')
    if type(name) is not str or name == "":
        return "invalid name", 400

    user_schema = UserSchema()

    fetched_user = users_collection.find_one({"name": name})

    if not fetched_user:

        new_user: User = User(None, name, [])
        new_user_serialized = user_schema.dump(new_user)

        users_collection.insert_one(new_user_serialized)

        fetched_user = new_user_serialized

    fetched_user = user_schema.dump(user_schema.load(fetched_user))
    return fetched_user, 200


@user_api.route('/users/collections', methods=['POST'])
def add_user_to_collection():
    username: str = request.args.get('username')
    collection_name: str = request.args.get('collection')

    collection = db.get_collection(collection_name)
    if collection is None:
        return "collection invalid", 400

    user_json = users_collection.find_one({"name": username})
    if user_json is None:
        return "user invalid", 400

    user: User = UserSchema().make_user(user_json)

    if collection_name in user.joined_collections:
        return "user already joined collection", 400


    users_collection.update_one({"name": username}, {"$set": {"joined_collections": user.joined_collections + [collection_name]}})
    return "user joined collection", 200

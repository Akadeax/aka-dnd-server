from typing import List
from bson import ObjectId
from marshmallow import Schema, fields, post_load, post_dump

from server.models.object_id_field import ObjectIdField

class User(object):
    id: ObjectId
    name: str
    joined_collections: List[str]

    def __init__(self, _id = None, name = "", joined_collections = []):
        self._id = _id
        self.name = name
        self.joined_collections = joined_collections

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class UserSchema(Schema):
    _id = ObjectIdField(required=False, allow_none=True)
    name = fields.Str(required=True)
    joined_collections = fields.List(fields.Str())

    @post_dump
    def _correct_id_in_dump(self, data, **kwargs):
        if "_id" in data and (data["_id"] is None or data["_id"] == ""):
            del data["_id"]

        return data

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

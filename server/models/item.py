from bson import ObjectId
from marshmallow import Schema, fields, post_load

from server.models.object_id_field import ObjectIdField

class Item(object):
    id: ObjectId
    name: str
    amount: int

    def __init__(self, _id = "", name = "", amount = 1):
        self._id = _id
        self.name = name
        self.amount = amount
    
    def __repr__(self):
        return '<Item(name={self.name!r})>'.format(self=self)


class ItemSchema(Schema):
    _id = ObjectIdField(required=False)
    name = fields.Str(required=True)
    amount = fields.Number(required=True)

    @post_load
    def make_item(self, data, **kwargs):
        return Item(**data)

from marshmallow import fields
from bson import ObjectId

class ObjectIdField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, ObjectId):
            return value

        if not isinstance(value, str) or value == "":
            return None

        return ObjectId(value)

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, ObjectId):
            return str(value)

        return None

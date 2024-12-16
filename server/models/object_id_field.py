from marshmallow import fields
from bson import ObjectId

class ObjectIdField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            return value
    
        if value == "":
            return ObjectId("000000000000000000000000")
        
        return ObjectId(value)

    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, ObjectId):
            return value
        
        return str(value)

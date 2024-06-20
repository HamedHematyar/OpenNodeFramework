from backend.aggregations import TypeCollection
from backend.data_types import (GenericNode,
                                GenericStr,
                                GenericNodeAttribute)
from backend.bases import BaseAttributeNode


class GenericAttribute(BaseAttributeNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        attributes = kwargs.pop('attributes', {})
        self.set_attributes(attributes or self.init_attributes())

        self.populate_data(**kwargs)

    def init_attributes(self):
        collection = TypeCollection()

        collection['parent'] = GenericNode()
        collection['value'] = GenericStr()
        collection['default'] = GenericStr()
        collection['label'] = GenericStr()
        collection['reference'] = GenericNodeAttribute()

        return collection

    def validate_attributes(self, attributes):
        return True

    @classmethod
    def deserialize_attributes(cls, data):
        return TypeCollection.deserialize(data, relations=True)

    def data(self):
        reference = self.attributes['reference'].data()

        if reference is None:
            return reference

        value = self.attributes['value'].data()
        if value is None:
            return value

        default = self.attributes['default'].data()
        return default

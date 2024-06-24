from backend.aggregations import AttributeTypesCollection
from backend.data_types import (ReferencedNode,
                                GenericStr,
                                ReferencedNodeAttribute)
from backend.bases import BaseAttributeNode


class GenericAttribute(BaseAttributeNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        attributes = kwargs.pop('attributes', {})
        self.set_attributes(attributes or self.init_attributes())

        self.populate_data(**kwargs)

    def init_attributes(self):
        collection = AttributeTypesCollection()

        collection['parent'] = ReferencedNode()
        collection['reference'] = ReferencedNodeAttribute()

        return collection

    def validate_attributes(self, attributes):
        return True

    @classmethod
    def deserialize_attributes(cls, data):
        return AttributeTypesCollection.deserialize(data, relations=True)

    def data(self):
        reference = self.attributes['reference']

        if reference is not None:
            return reference.data()


class StringAttribute(GenericAttribute):
    def init_attributes(self):
        collection = super().init_attributes()

        collection['value'] = GenericStr()
        collection['label'] = GenericStr()
        collection['default'] = GenericStr()

        return collection

    def data(self):
        super_result = super().data()
        if super_result is not None:
            return super_result

        value = self.attributes['value'].data()
        if value is not None:
            return value

        default = self.attributes['default'].data()
        return default

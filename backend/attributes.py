import typing as t

from backend.registry import register_attribute
from backend.aggregations import DataTypeCollection
from backend.data_types import (ReferencedNode,
                                GenericStr,
                                GenericInt,
                                ReferencedNodeAttribute)
from backend.bases import BaseAttributeNode


class GenericAttribute(BaseAttributeNode):

    def init_attributes(self):
        collection = DataTypeCollection()

        collection['parent'] = ReferencedNode()
        collection['reference'] = ReferencedNodeAttribute()

        return collection

    def validate_attributes(self, attributes):
        return True

    @classmethod
    def deserialize_attributes(cls, data):
        from backend import registry
        subclass: t.Optional[t.Type[DataTypeCollection]] = registry.registered_type(registry.Category.COLLECTION,
                                                                                    data['class'])

        return {'attributes': subclass.deserialize(data)}

    def data(self):
        reference = self.attributes['reference']

        if reference is not None:
            return reference.data()


@register_attribute
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


@register_attribute
class IntAttribute(GenericAttribute):
    def init_attributes(self):
        collection = super().init_attributes()

        collection['value'] = GenericInt()
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
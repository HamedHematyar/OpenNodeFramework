from backend.aggregations import TypeCollection
from backend.data_types import (GenericNode,
                                GenericStr,
                                GenericNodeAttribute)
from backend.bases import BaseAttributeNode


class GenericAttribute(BaseAttributeNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(TypeCollection())

        self.attributes['parent'] = GenericNode()
        self.attributes['name'] = GenericStr()
        self.attributes['value'] = GenericStr()
        self.attributes['default'] = GenericStr()
        self.attributes['label'] = GenericStr()
        self.attributes['reference'] = GenericNodeAttribute()

        self.populate_data(**kwargs)

    def populate_data(self, **kwargs):
        for key, value in kwargs.items():
            if self.attributes.get(key):
                self.attributes[key].set_data(value)

    def validate_attributes(self, attributes):
        return True

    def data(self):
        reference = self.attributes['reference'].data()

        if reference is None:
            return reference

        value = self.attributes['value'].data()
        if value is None:
            return value

        default = self.attributes['default'].data()
        return default

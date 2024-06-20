from backend.aggregations import TypeCollection
from backend.data_types import (GenericNode,
                                GenericStr,
                                GenericNodeAttribute)
from backend.bases import BaseAttributeNode


class GenericAttribute(BaseAttributeNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_types(TypeCollection())

        self.types['parent'] = GenericNode()
        self.types['name'] = GenericStr()
        self.types['value'] = GenericStr()
        self.types['default'] = GenericStr()
        self.types['label'] = GenericStr()
        self.types['reference'] = GenericNodeAttribute()

        self.populate_data(**kwargs)

    def populate_data(self, **kwargs):
        for key, value in kwargs.items():
            if self.types.get(key):
                self.types[key].set_data(value)

    def validate_types(self, types):
        return True

    def data(self):
        reference = self.types['reference'].data()

        if reference is None:
            return reference

        value = self.types['value'].data()
        if value is None:
            return value

        default = self.types['default'].data()
        return default

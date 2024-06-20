from backend.aggregations import TypeCollection
from backend.data_types import (GenericNode,
                                GenericStr,
                                GenericNodeAttribute)
from backend.bases import BaseAttributeNode


class GenericAttribute(BaseAttributeNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_types(TypeCollection())

        self.types.append(GenericNode(name='parent'))
        self.types.append(GenericStr(name='name'))
        self.types.append(GenericStr(name='value'))
        self.types.append(GenericStr(name='default'))
        self.types.append(GenericStr(name='label'))
        self.types.append(GenericNodeAttribute(name='reference'))

    def data(self):
        reference = self.types['reference'].data()

        if reference is None:
            return reference

        value = self.types['value'].data()
        if value is None:
            return value

        default = self.types['default'].data()
        return default 

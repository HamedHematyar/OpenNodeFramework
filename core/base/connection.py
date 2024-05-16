from core.registry import *
from core.base.attribute import *
from core.abstract.connection import *


class Wire(AbstractConnection):
    def __init__(self):
        self._source_attribute: Attribute or None = None
        self._destination_attribute: Attribute or None = None

    def get_source(self) -> Attribute:
        return self._source_attribute

    def get_valid_source_types(self) -> typing.List[Attribute]:
        return Attributes

    def get_destination(self) -> Attribute:
        return self._destination_attribute

    def get_valid_destination_types(self) -> typing.List[Attribute]:
        return Attributes


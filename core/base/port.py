from core.registry import *
from core.base.node import *
from core.abstract.port import *


class Port(AbstractPort):
    def __init__(self):
        self._source_attribute: Attribute or None = None
        self._destination_attribute: Attribute or None = None

    def get_source(self) -> AbstractNode:
        return self._source_attribute

    def get_valid_source_types(self) -> typing.List[AbstractNode]:
        return Nodes

    def get_destination(self) -> AbstractNode:
        return self._destination_attribute

    def get_valid_destination_types(self) -> typing.List[AbstractNode]:
        return Nodes


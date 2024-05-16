import typing

from core.registry import *
from core.base.attribute import *
from core.abstract.connection import *


class Connection(AbstractConnection):
    def __init__(self, source, destination):
        self._source: typing.Optional[Attribute] = source
        self._destination: typing.Optional[Attribute] = destination

    def get_source(self) -> Attribute:
        return self._source

    def get_destination(self) -> Attribute:
        return self._destination

    def get_data(self) -> typing.Any:
        return self._source.get_value()

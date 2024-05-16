from abc import ABC, abstractmethod
import typing

from core.base.attribute import *


class AbstractWire(ABC):
    """
    An abstract class representing a plug.
    """

    @abstractmethod
    def get_source(self) -> Attribute:
        """This should return the source node of the plug."""

    @abstractmethod
    def get_valid_source_types(self) -> typing.List[Attribute]:
        """This should return a list of valid source attribute types."""

    @abstractmethod
    def get_destination(self) -> Attribute:
        """This should return the destination node of the plug."""

    def get_valid_destination_types(self) -> typing.List[Attribute]:
        """This should return a list of valid destination attribute types."""

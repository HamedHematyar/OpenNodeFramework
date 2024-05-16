import typing
from abc import ABC, abstractmethod

from core.base.attribute import *


class AbstractConnection(ABC):
    """
    An abstract class representing a node connection.
    """

    @abstractmethod
    def get_source(self) -> Attribute:
        """This should return the source attribute of the connection."""

    @abstractmethod
    def get_valid_source_types(self) -> typing.List[Attribute]:
        """This should return a list of valid source attribute types."""

    @abstractmethod
    def get_destination(self) -> Attribute:
        """This should return the destination attribute of the connection."""

    def get_valid_destination_types(self) -> typing.List[Attribute]:
        """This should return a list of valid destination attribute types."""

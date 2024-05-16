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
    def get_destination(self) -> Attribute:
        """This should return the destination attribute of the connection."""

    @abstractmethod
    def get_data(self) -> typing.Any:
        """This should give access to connection data"""

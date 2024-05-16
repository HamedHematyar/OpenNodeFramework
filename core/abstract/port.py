import typing
from abc import ABC, abstractmethod

from core.abstract.node import *


class AbstractPlug(ABC):
    """
    An abstract class representing a node port.
    """

    @abstractmethod
    def get_source(self) -> AbstractNode:
        """This should return the source node of the port."""

    @abstractmethod
    def get_valid_source_types(self) -> typing.List[AbstractNode]:
        """This should return a list of valid source node types."""

    @abstractmethod
    def get_destination(self) -> AbstractNode:
        """This should return the destination node of the port."""

    def get_valid_destination_types(self) -> typing.List[AbstractNode]:
        """This should return a list of valid destination node types."""

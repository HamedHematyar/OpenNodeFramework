from abc import ABC, abstractmethod

from core.abstract.node import *


class AbstractPlug(ABC):
    """
    An abstract class representing a plug.
    """

    @abstractmethod
    def get_source(self) -> AbstractNode:
        """This should return the source node of the plug."""

    @abstractmethod
    def get_destination(self) -> AbstractNode:
        """This should return the destination node of the plug."""

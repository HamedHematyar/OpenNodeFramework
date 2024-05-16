import typing
from abc import ABC, abstractmethod


class AbstractAttribute(ABC):
    """
    An abstract class representing a node attribute.
    """
    @abstractmethod
    def set_name(self, name: str) -> bool:
        """This method set the name of the attribute """

    @abstractmethod
    def get_name(self) -> str:
        """This method return the name of the attribute"""

    def set_value(self, value: typing.Any) -> bool:
        """This method set the value of the attribute """

    def get_value(self) -> typing.Any:
        """This method return the value of the attribute"""

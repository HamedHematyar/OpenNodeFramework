import typing as t

from abc import ABC, abstractmethod

from backend.enums import PortType


class AbstractAttribute(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """This returns the name of the attribute."""

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """This sets the name of the attribute."""

    @property
    @abstractmethod
    def node(self) -> 'AbstractNode':
        """This returns the value of the parent node."""

    @node.setter
    @abstractmethod
    def node(self, value: 'AbstractNode'):
        """This sets the value of the parent node."""

    def __del__(self):
        """This method is called when this class is deleted."""

    @abstractmethod
    def get_value(self) -> t.Any:
        """This returns the value of the attribute."""

    @abstractmethod
    def set_value(self, value: t.Any):
        """This sets the value of the attribute."""


class AbstractPort(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """This should return the name of the port."""
    @name.setter
    @abstractmethod
    def name(self, name: str):
        """This should set the name of the port."""

    @property
    @abstractmethod
    def mode(self) -> t.Optional[PortType]:
        """This should return the mode of the port."""

    @mode.setter
    @abstractmethod
    def mode(self, _type: PortType):
        """This should set the mode of the port."""

    @property
    @abstractmethod
    def node(self) -> t.Optional['AbstractNode']:
        """This should return the node of the port."""

    @node.setter
    @abstractmethod
    def node(self, node: 'AbstractNode'):
        """This should set the node of the port."""

    def __del__(self):
        """This method is called when this class is deleted."""


class AbstractNode(ABC):

    @abstractmethod
    def data(self) -> t.Optional[t.Any]:
        """This method computes the node data"""

    def __del__(self):
        """This method is called when this class is deleted."""


class AbstractGraph(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """This returns the name of the graph."""

    @name.setter
    @abstractmethod
    def name(self, name: str):
        """This sets the name of the graph."""

    def __del__(self):
        """This method is called when this class is deleted."""

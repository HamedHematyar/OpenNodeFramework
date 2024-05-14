from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractAttribute(ABC):
    """
    An abstract class representing an attribute.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Property that should return the name of the attribute.
        """
        raise NotImplementedError('must override this method')

    @property
    @abstractmethod
    def value(self) -> Any:
        """
        Property that should return the value of the attribute.
        """
        raise NotImplementedError('must override this method')


class AbstractAttributeCollection(ABC):
    """
    An abstract class representing a manager for a list of attribute.
    """

    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """
        Method that should return a dictionary representation of the attribute managed by this instance.
        """
        raise NotImplementedError('must override this method')

    @abstractmethod
    def deserialize(self, attributes_data: Dict[str, Any]) -> None:
        """
        Method that should parse a dictionary representation of attribute and update this instance's attribute
        accordingly.

        :param attributes_data: A dictionary of attribute data, typically coming from a call to 'serialize'.
        """
        raise NotImplementedError('must override this method')

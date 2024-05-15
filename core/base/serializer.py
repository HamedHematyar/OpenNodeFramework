from typing import Dict, Any

from core import registry
from core.abstract import attribute
from core.abstract import serializer


class AttributeSerializer(serializer.AbstractAttributeSerializer):

    def serialize(self, attr: attribute.AbstractAttribute) -> Dict[str, Any]:
        """
        Test the serialize method with a sample attribute object
        >>> from core.concrete import attribute
        >>> attr_instance = attribute.NameAttribute(value='test')

        >>> serializer_instance = AttributeSerializer()
        >>> serializer_instance.serialize(attr_instance)
        {'type': 'NameAttribute', 'name': 'name', 'value': 'test'}
        """

        data = {"type": attr.__class__.__name__}
        data.update(dict(attr))

        return data

    def deserialize(self, attr_data: Dict[str, Any]) -> attribute.AbstractAttribute:
        """
        Test the deserialize method with a sample attribute dict

        >>> data = {'type': 'NameAttribute', 'name': 'name', 'value': 'test'}
        >>> serializer_instance = AttributeSerializer()
        >>> attr_instance = serializer_instance.deserialize(data)
        >>> isinstance(attr_instance, attribute.AbstractAttribute)
        True
        """
        attr_type = attr_data.pop('type')
        attr = registry.Attributes[attr_type](**attr_data)

        return attr


class AbstractAttributeCollectionSerializer(serializer.AbstractAttributeCollectionSerializer):
    def serialize(self, attr_collection: attribute.AbstractAttributeCollection) -> Dict[str, Any]:
        pass

    def deserialize(self, attr_data: Dict[str, Any]) -> attribute.AbstractAttributeCollection:
        pass
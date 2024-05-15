from core.registry import *
from core.base.attribute import *
from core.abstract.serializer import *


class AttributeSerializer(AbstractAttributeSerializer):

    def serialize(self, attr: Attribute) -> Dict[str, Any]:
        return {"type": attr.__class__.__name__, **attr}

    def deserialize(self, attr_data: Dict[str, Any]) -> Attribute:
        return Attributes[attr_data.pop('type')](**attr_data)


class AttributeCollectionSerializer(AbstractAttributeCollectionSerializer):
    def serialize(self, collection_instance: AttributeCollection) -> Dict[str, Any]:
        data = {}
        for key, attr in collection_instance.items():
            serialized_attr = AttributeSerializer().serialize(attr)
            data.update({key: serialized_attr})

        return data

    def deserialize(self, collection_data: Dict[str, Any]) -> AttributeCollection:

        collection = AttributeCollection()
        for key, attribute_data in collection_data.items():
            attribute_serializer = AttributeSerializer()
            deserialized_attr = attribute_serializer.deserialize(attribute_data)

            collection.update_from_attribute(deserialized_attr)

        return collection




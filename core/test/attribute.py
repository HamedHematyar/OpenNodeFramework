from core.concrete.attribute import *
from core.base.serializer import *

if __name__ == '__main__':
    attr_01 = StringAttribute(name="name", value="node_name")
    print(attr_01)

    attr_01_serializer = AttributeSerializer()
    print(attr_01_serializer)

    serialized_attr_01 = attr_01_serializer.serialize(attr_01)
    print(serialized_attr_01)

    deserialized_attr_01 = attr_01_serializer.deserialize(serialized_attr_01)
    print(deserialized_attr_01)

    assert attr_01 is not deserialized_attr_01

    attr_02 = StringAttribute(name="path", value="node/path")
    print(attr_02)

    attr_collection = AttributeCollection()
    attr_collection.add(attr_01)
    attr_collection.add(attr_02)

    print(attr_collection)

    collection_serializer = AttributeCollectionSerializer()
    print(collection_serializer)

    serialized_collection = collection_serializer.serialize(attr_collection)
    print(serialized_collection)

    deserialized_collection = collection_serializer.deserialize(serialized_collection)
    print(deserialized_collection)

    assert attr_collection is not deserialized_collection




from backend.attributes import GenericStr, GenericInt
from backend.aggregations import AttributeCollection


if __name__ == '__main__':
    attr_01 = GenericStr(name='name', value='test_name')
    print(attr_01.dumps(indent=4))

    serialized_attribute = attr_01.serialize()
    print(serialized_attribute)

    deserialized_attribute = GenericStr.deserialize(serialized_attribute, relations=True)
    print(deserialized_attribute.dumps(indent=4))

    path = "../dump/attribute.json"
    dumped_attribute = attr_01.dump(path, indent=4)

    loaded_attribute = GenericStr.load(path)
    print(loaded_attribute.dumps(indent=4))

    attr_02 = GenericStr(name='label', value="name")
    attr_03 = GenericInt(name='size', value=5)

    attr_collection = AttributeCollection()
    attr_collection.append(attr_01)
    attr_collection.append(attr_02)
    attr_collection.append(attr_03)

    print(attr_collection.dumps(indent=4))

    serialized_collection = attr_collection.serialize()
    print(serialized_collection)

    deserialized_collection = AttributeCollection.deserialize(serialized_collection, relations=True)
    print(deserialized_collection.dumps(indent=4))

    path = "../dump/attribute_collection.json"
    dumped_collection = attr_collection.dump(path, indent=4)

    loaded_collection = AttributeCollection.load(path)
    print(loaded_collection.dumps(indent=4))
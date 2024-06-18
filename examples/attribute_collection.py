from backend.attributes import GenericInt, GenericStr
from backend.aggregations import AttributeCollection

attribute_collection = AttributeCollection()

int_constant_01 = GenericInt(name='int_constant', value=10)
str_constant_02 = GenericStr(name='str_constant', value='test')

attribute_collection.append(int_constant_01)
attribute_collection.append(str_constant_02)

serialized = attribute_collection.serialize()
print(serialized)


deserialized = attribute_collection.deserialize(serialized, relations=True)
print(deserialized)

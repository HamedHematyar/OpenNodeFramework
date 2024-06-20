import pathlib

from backend.data_types import GenericStr, GenericInt
from backend.aggregations import TypeCollection


if __name__ == '__main__':

    collection = TypeCollection()
    collection['label'] = GenericStr(data="label")
    collection['size'] = GenericInt(data=5)

    print(collection.dumps(indent=4))

    serialized_collection = collection.serialize()
    print(serialized_collection)

    deserialized_collection = TypeCollection.deserialize(serialized_collection, relations=True)
    print(deserialized_collection.dumps(indent=4))

    path = pathlib.Path("../dump/types/type_collection.json")
    dumped_collection = collection.dump(path, indent=4)

    loaded_collection = TypeCollection.load(path, relations=True)
    print(loaded_collection.dumps(indent=4))

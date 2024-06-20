import pathlib
import unittest

from backend.data_types import GenericStr, GenericInt
from backend.aggregations import TypeCollection


class TestTypeCollection(unittest.TestCase):
    def setUp(self):
        self.collection = TypeCollection()

        self.collection['label'] = GenericStr(data="label")
        self.collection['size'] = GenericInt(data=5)

        self.path = pathlib.Path("../dump/types/type_collection.json")

    def test_initial_items(self):
        self.assertEqual(len(self.collection.items()), 2)
        self.assertIn('label', self.collection)
        self.assertIn('size', self.collection)

    def test_item_data(self):
        self.assertEqual(self.collection['size'].data(), 5)

    def test_serialization(self):
        serialized_collection = self.collection.serialize()
        self.assertIn('items', serialized_collection)

    def test_deserialization(self):
        serialized_collection = self.collection.serialize()

        # test with relations
        deserialized_collection = TypeCollection.deserialize(serialized_collection, relations=True)
        self.assertIn(self.collection['label'], deserialized_collection.values())

        # test with not relations
        deserialized_collection = TypeCollection.deserialize(serialized_collection, relations=False)
        self.assertNotIn(self.collection['label'], deserialized_collection.values())

    def test_dump_and_load(self):
        self.collection.dump(self.path, indent=4)
        self.assertTrue(pathlib.Path(self.path).exists())

        # test with relations
        loaded_collection = TypeCollection.load(self.path, relations=True)
        self.assertIn(self.collection['label'], loaded_collection.values())

        # test with not relations
        loaded_collection = TypeCollection.load(self.path, relations=False)
        self.assertNotIn(self.collection['label'], loaded_collection.values())


if __name__ == '__main__':
    unittest.main()

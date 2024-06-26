import pathlib
import unittest

from backend.meta import InstanceManager
from backend.data_types import GenericStr
from backend.attributes import StringAttribute
from backend.aggregations import AttributeCollection


class TestAttributeNode(unittest.TestCase):
    def setUp(self):
        self.collection = AttributeCollection()
        self.dump_path = pathlib.Path("../dump/attributes/attribute_collection.json")

    def test_dump_and_load(self):
        driver = StringAttribute(value='driver')

        driven = StringAttribute(value='driven')
        driven.attributes['reference'].set_data(driver)

        self.collection['driver'] = driver
        self.collection['driven'] = driven

        self.collection.dump(self.dump_path, indent=4)

        InstanceManager().clear_all()

        loaded_collection = AttributeCollection.load(self.dump_path)
        self.assertEqual(len(self.collection), len(loaded_collection))
        self.assertEqual(self.collection['driver'].data(), loaded_collection['driver'].data())
        self.assertEqual(self.collection['driven'].data(), loaded_collection['driven'].data())
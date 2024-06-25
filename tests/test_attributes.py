import pathlib
import unittest

from backend.meta import ReferenceManager, InstanceManager
from backend.data_types import GenericStr
from backend.attributes import StringAttribute


class TestAttributeNode(unittest.TestCase):
    def test_attribute_default(self):
        attribute_node = StringAttribute(default='default')
        self.assertTrue(attribute_node.data(), 'default')

    def test_attribute_data(self):
        attribute_node = StringAttribute(value='hello', default='default')
        self.assertTrue(attribute_node.data(), 'hello')

    def test_add_type(self):
        attribute_node = StringAttribute(value='hello', default='default')
        attribute_node.attributes['runtime_type'] = GenericStr(data='username')

        self.assertTrue(attribute_node.attributes, 'runtime_type')

    def test_serialization(self):
        attribute_node = StringAttribute(value='hello', default='default')
        attribute_node.attributes['runtime_type'] = GenericStr(data='username')

        self.assertIsInstance(attribute_node.serialize(), dict)
        self.assertIn('runtime_type', attribute_node.serialize()['attributes'])
        self.assertIn('value', attribute_node.serialize()['attributes'])

    def test_serialization_and_deserialization(self):
        driver = StringAttribute(value='driver')
        driven = StringAttribute(value='driven')

        driven.attributes['reference'].set_data(driver)
        self.assertTrue(driven.attributes['reference'].get_data(serialize=True), driver)
        self.assertEqual(driver.get_id(), driven.serialize()['attributes']['reference']['data'])

        deserialized_driven = StringAttribute.deserialize(driven.serialize(), relations=True)
        self.assertTrue(deserialized_driven.attributes['reference'].get_data(serialize=True), driver)

    def test_dump_and_load(self):
        driver = StringAttribute(value='driver')

        driven = StringAttribute(value='driven')
        driven.attributes['reference'].set_data(driver)

        driven_path = pathlib.Path("../dump/attributes/driven_attribute.json")
        driver_path = pathlib.Path("../dump/attributes/driver_attribute.json")

        driven.dump(driven_path, indent=4)
        driver.dump(driver_path, indent=4)

        loaded_driver = StringAttribute.load(driver_path, relations=True)
        loaded_driven = StringAttribute.load(driven_path, relations=True)

        # driver object is still live so referencing to that not the loaded one
        self.assertEqual(driver.get_id(), loaded_driven.attributes['reference'].data())

        InstanceManager().clear_all()
        with ReferenceManager() as reference_manager:
            loaded_driver = StringAttribute.load(driver_path, relations=True)
            loaded_driven = StringAttribute.load(driven_path, relations=True)

        # driver object is loaded so referencing that
        self.assertEqual(loaded_driver.get_id(), loaded_driven.attributes['reference'].data())


if __name__ == '__main__':
    unittest.main()

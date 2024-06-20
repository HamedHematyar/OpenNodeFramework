import pathlib
import unittest
from backend.data_types import GenericInt
from backend.meta import InstanceManager


class TestGenericInt(unittest.TestCase):
    def setUp(self):
        self.constant = GenericInt()
        self.path = pathlib.Path("../dump/types/constant.json")

    def test_1_instance_tracking(self):
        self.assertIn(self.constant.get_id(), InstanceManager().instances())

        deserialized_constant = GenericInt.deserialize(self.constant.serialize())
        loaded_constant = GenericInt.load(self.path)

        self.assertEqual(len(InstanceManager().instances()), 3)

        self.constant.delete()
        deserialized_constant.delete()
        loaded_constant.delete()

        self.assertEqual(len(InstanceManager().instances()), 0)

    def test_create_no_data(self):
        constant = GenericInt()
        self.assertEqual(constant.data(), constant.default)

        constant.delete()

    def test_create_with_data(self):
        constant = GenericInt(data=10)
        self.assertEqual(constant.data(), 10)

        constant.delete()

    def test_delete(self):
        constant = GenericInt(data=10)
        self.assertEqual(constant.data(), 10)

        constant.delete()
        self.assertNotIn(constant, InstanceManager().instances().values())

    def test_get_data(self):
        self.constant = GenericInt(data=30)
        self.assertEqual(self.constant.data(), 30)
        self.assertEqual(self.constant.get_data(), 30)

    def test_set_data_valid(self):
        self.assertTrue(self.constant.set_data(40))
        self.assertEqual(self.constant.data(), 40)

    def test_set_data_invalid(self):
        self.assertTrue(self.constant.set_data(40))

        self.assertFalse(self.constant.set_data('hello'))
        self.assertEqual(self.constant.data(), 40)

    def test_data_casting(self):
        self.assertTrue(self.constant.set_data(13.5))
        self.assertEqual(self.constant.data(), 13)

    def test_direct_data_validation(self):
        self.assertFalse(self.constant.validate_data('hello'))
        self.assertTrue(self.constant.validate_data(12))

    def test_delete_data(self):
        self.constant.del_data()
        self.assertEqual(self.constant.data(), self.constant.default)

    def test_serialization(self):
        serialized_constant = self.constant.serialize()
        self.assertIn('data', serialized_constant)
        self.assertTrue(self.constant.get_id(), serialized_constant.get('id'))

    def test_deserialization(self):
        serialized_constant = self.constant.serialize()
        deserialized_constant = GenericInt.deserialize(serialized_constant)

        self.assertNotEqual(deserialized_constant.get_id(), self.constant.get_id())

    def test_dump_and_load(self):
        self.assertTrue(self.constant.set_data(25))

        self.constant.dump(self.path, indent=4)
        self.assertTrue(self.path.is_file())

        loaded_constant = GenericInt.load(self.path)
        self.assertEqual(self.constant.data(), 25)
        self.assertNotEqual(loaded_constant.get_id(), self.constant.get_id())


if __name__ == '__main__':
    unittest.main()

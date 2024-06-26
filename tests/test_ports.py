import pathlib
import unittest

from backend.meta import InstanceManager, ReferenceManager
from backend.data_types import GenericStr
from backend.ports import InputPort, OutputPort


class TestAttributeNode(unittest.TestCase):
    def test_create_port(self):
        port_node = InputPort(label='test_input')

        self.assertTrue(port_node.get_id(), True)

    def test_port_data(self):
        port_node = InputPort(label='test_input')
        self.assertTrue(port_node.attributes['label'].data(), 'test_input')
        self.assertTrue(port_node.attributes['mode'].data(), 'INPUT')

    def test_add_custom_data(self):
        port_node = InputPort(label='test_input')

        custom_data = GenericStr(data='test_data')
        port_node.attributes['custom_data'] = custom_data

        self.assertTrue(port_node.attributes['custom_data'].data(), 'test_data')

    def test_add_connection(self):
        out_port = OutputPort(label='test_output', mode='OUTPUT')
        in_port = InputPort(label='test_input', mode='INPUT')

        in_port.attributes['connections'].set_data([out_port])

        self.assertIn(out_port.get_id(), in_port.attributes['connections'].data())

    def test_serialization(self):
        out_port = OutputPort(label='test_output')
        in_port = InputPort(label='test_input')

        in_port.attributes['connections'].set_data([out_port])

        self.assertIsInstance(in_port.serialize(), dict)

    def test_serialization_and_deserialization(self):
        out_port = OutputPort(label='test_output', mode='OUTPUT')
        in_port = InputPort(label='test_input', mode='INPUT')

        in_port.attributes['connections'].set_data([out_port])

        deserialized_in_port = InputPort.deserialize(in_port.serialize())
        self.assertIn(out_port.get_id(), deserialized_in_port.attributes['connections'].data())

    def test_dump_and_load(self):
        out_port = OutputPort(label='test_output', mode='OUTPUT')
        in_port = InputPort(label='test_input', mode='INPUT')

        in_port.attributes['connections'].set_data([out_port])

        in_port_path = pathlib.Path("../dump/ports/input_port.json")
        in_port.dump(in_port_path, indent=4)

        out_port_path = pathlib.Path("../dump/ports/output_port.json")
        out_port.dump(out_port_path, indent=4)

        loaded_in_port = InputPort.load(in_port_path)
        loaded_out_port = OutputPort.load(out_port_path)

        # out_port object is still live so referencing to that not the loaded one
        self.assertIn(out_port.get_id(), loaded_in_port.attributes['connections'].data())

        InstanceManager().clear_all()
        with ReferenceManager() as reference_manager:
            loaded_out_port = OutputPort.load(out_port_path)
            loaded_in_port = InputPort.load(in_port_path)

        # driver object is loaded so referencing that
        self.assertIn(loaded_out_port.get_id(), loaded_in_port.attributes['connections'].data())


if __name__ == '__main__':
    unittest.main()

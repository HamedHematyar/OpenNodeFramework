from backend.data_types import GenericNode, GenericStr, PortModeEnum, GenericList
from backend.bases import BasePortNode
from backend.aggregations import PortCollection, PortAttributesCollection


class GenericPort(BasePortNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(PortAttributesCollection())

        self.attributes['parent'] = GenericNode()
        self.attributes['label'] = GenericStr()
        self.attributes['mode'] = PortModeEnum()

        self.populate_data(**kwargs)

    def populate_data(self, **kwargs):
        for key, value in kwargs.items():
            if self.attributes.get(key):
                self.attributes[key].set_data(value)

    def validate_attributes(self, attributes):
        return True

    def data(self):
        return


class InputPort(GenericPort):
    relation_attributes = ['attributes',
                           'inputs']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._inputs = None

        self.set_inputs(PortCollection())
        self.attributes['mode'].set_data('INPUT')

    @property
    def inputs(self):
        return self.get_inputs()

    def get_inputs(self, serialize=False):
        if serialize:
            return self._inputs.serialize()

        return self._inputs

    def set_inputs(self, inputs):
        if not self.validate_inputs(inputs):
            return False

        self._inputs = inputs
        return True

    def del_inputs(self):
        self._inputs.clear()

    def validate_inputs(self, inputs):
        return True

    def deserialize_inputs(self, data):
        return self._inputs.deserialize(data, relations=True)


class OutputPort(GenericPort):
    relation_attributes = ['attributes',
                           'outputs']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._outputs = None

        self.set_outputs(PortCollection())
        self.attributes['mode'].set_data('OUTPUT')

    @property
    def outputs(self):
        return self.get_outputs()

    def get_outputs(self, serialize=False):
        if serialize:
            return self._outputs.serialize()

        return self._outputs

    def set_outputs(self, outputs):
        if not self.validate_outputs(outputs):
            return False

        self._outputs = outputs
        return True

    def del_outputs(self):
        self._outputs.clear()

    def validate_outputs(self, outputs):
        return True

    def deserialize_outputs(self, data):
        return self._outputs.deserialize(data, relations=True)
    
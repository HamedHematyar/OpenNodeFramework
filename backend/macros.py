from backend.aggregations import NodeCollection, AttributeCollection, PortCollection
from backend.bases import BaseMacroNode


class GenericMacro(BaseMacroNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_attributes(AttributeCollection())
        self.set_inputs(PortCollection())
        self.set_outputs(PortCollection())
        self.set_nodes(NodeCollection())

    def validate_attributes(self, attributes):
        return True

    def validate_inputs(self, inputs):
        return True

    def validate_outputs(self, outputs):
        return True

    def validate_nodes(self, nodes):
        return True

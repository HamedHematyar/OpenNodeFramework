from backend.bases import BasePort
from backend.aggregations import PortCollection


class InputPort(BasePort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_connections(PortCollection())

    def data(self, connection_index=0):
        return self.get_connections()[connection_index].data()


class OutputPort(BasePort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_connections(PortCollection())

    def data(self, connection_index=0):
        return self.get_parent().data()

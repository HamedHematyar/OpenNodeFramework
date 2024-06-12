from backend.bases import BasePort


class InputPort(BasePort):
    def __init__(self):
        super().__init__()

    def data(self, connection_index=0):
        return self.connections[connection_index].data()


class OutputPort(BasePort):
    def __init__(self):
        super().__init__()

    def data(self, connection_index=0):
        return self.node.data()
    
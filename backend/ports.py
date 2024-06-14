from backend.bases import BasePort


class InputPort(BasePort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def data(self, connection_index=0):
        return self.connections[connection_index].data()


class OutputPort(BasePort):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def data(self, connection_index=0):
        return self.get_parent().data()
    
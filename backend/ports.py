from backend.bases import BasePort


class InPort(BasePort):
    def __init__(self, name, mode):
        super().__init__(name, mode)


class OutPort(BasePort):
    def __init__(self, name, mode):
        super().__init__(name, mode)

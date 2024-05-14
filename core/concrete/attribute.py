from core.base import attribute


class NameAttribute(attribute.Attribute):
    def __init__(self, name, value):
        super().__init__(name, value)


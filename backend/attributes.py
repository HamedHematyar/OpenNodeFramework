from backend.bases import BaseAttribute


class String(BaseAttribute):
    def __init__(self):
        super().__init__()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, str):
            raise TypeError(f'attribute value must be a str.')

        self.__value = value


class Integer(BaseAttribute):
    def __init__(self):
        super().__init__()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'attribute value must be a int.')

        self.__value = value


class List(BaseAttribute):
    def __init__(self):
        super().__init__()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not isinstance(value, list):
            raise TypeError(f'attribute value must be a list.')

        self.__value = value


class TypeAttribute(BaseAttribute):
    def __init__(self):
        super().__init__()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if isinstance(value, str):
            value = eval(value)

        if value not in [str,
                         int,
                         list]:
            raise TypeError(f'attribute value is not valid.')

        self.__value = value.__name__


class NameAttribute(String):
    def __init__(self):
        super().__init__()

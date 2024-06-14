
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class EntityTrackerMeta(type):
    TYPE = None

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        InstanceManager().add_instance(cls, instance)
        return instance


class InstanceManager(metaclass=SingletonMeta):
    def __init__(self):
        self._instances = {}

    def add_instance(self, cls, instance):
        if cls.TYPE not in self._instances:
            self._instances[cls.TYPE] = {}

        if cls not in self._instances[cls.TYPE]:
            self._instances[cls.TYPE][cls] = []

        self._instances[cls.TYPE][cls].append(instance)

    def instances(self):
        return self._instances

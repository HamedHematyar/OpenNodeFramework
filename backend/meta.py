import uuid


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
        # get existing id or generate a new one
        unique_id = kwargs.get('id', str(uuid.uuid4()))

        # if this is in app deserialization we need a new id
        if not InstanceManager().is_valid(unique_id):
            unique_id = str(uuid.uuid4())

        kwargs.update({'id': unique_id})

        # initialize entity instance
        instance = super().__call__(*args, **kwargs)

        # add instance to the manager
        InstanceManager().add_instance(instance)

        return instance


class InstanceManager(metaclass=SingletonMeta):
    def __init__(self):
        self._instances = {}

    def is_valid(self, unique_id):
        return bool(not self._instances.get(unique_id))

    def add_instance(self, instance):
        self._instances[instance.get_id()] = instance

    def remove_instance(self, instance):
        self._instances.pop(instance.get_id())

    def get_instance(self, instance_id):
        return self._instances.get(instance_id)

    def instances(self):
        return self._instances

    def clear_all(self):
        self._instances.clear()
import uuid

from backend.logger import logger


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
        if instance.get_id() in self._instances:
            self._instances.pop(instance.get_id())
        else:
            logger.warning(f'instance does not exist or already removed : {instance.get_id()}')

    def get_instance(self, instance_id):
        return self._instances.get(instance_id)

    def instances(self):
        return self._instances

    def clear_all(self):
        self._instances.clear()


class ReferenceManager(metaclass=SingletonMeta):
    def __init__(self):
        self._references = {}

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._resolve_references()
        self._references.clear()

    def request_instant_reference(self, instance_id):
        return InstanceManager().get_instance(instance_id)

    def request_deferred_reference(self, instance_id, reference_setter):
        if not instance_id:
            return

        if not reference_setter:
            return

        self._request_reference(instance_id, reference_setter)

    def _request_reference(self, instance_id, reference_setter):
        logger.debug(f'requesting deferred reference : {instance_id} : {reference_setter}')

        if instance_id in self._references:
            self._references[instance_id].append(reference_setter)
        else:
            self._references[instance_id] = [reference_setter, ]

    def _resolve_references(self):
        for instance_id, setters in self._references.items():
            instance = InstanceManager().get_instance(instance_id)
            if not instance:
                logger.error(f'reference instance does not exist: {instance_id}')
                continue

            for setter in setters:
                logger.debug(f'resolving reference : {instance} : {setter}')
                setter(instance)


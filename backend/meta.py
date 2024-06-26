import uuid
import typing as t

from backend.logger import logger


class SingletonMeta(type):
    _instances: t.Dict[type, t.Any] = {}

    def __call__(cls, *args, **kwargs) -> t.Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class EntityTrackerMeta(type):

    def __init__(cls, name, bases, dct) -> None:
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs) -> t.Any:
        unique_id = kwargs.get('id', str(uuid.uuid4()))

        if not InstanceManager().is_valid(unique_id):
            unique_id = str(uuid.uuid4())

        kwargs.update({'id': unique_id})
        instance = super().__call__(*args, **kwargs)
        InstanceManager().add_instance(instance)
        return instance


class InstanceManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._instances: t.Dict[str, t.Any] = {}

    def is_valid(self, unique_id: str) -> bool:
        return unique_id not in self._instances

    def add_instance(self, instance: t.Any) -> None:
        self._instances[instance.get_id()] = instance

    def remove_instance(self, instance: t.Any) -> None:
        instance_id = instance.get_id()
        if instance_id in self._instances:
            self._instances.pop(instance_id)
        else:
            logger.warning(f'Instance does not exist or already removed: {instance_id}')

    def get_instance(self, instance_id: str) -> t.Optional[t.Any]:
        return self._instances.get(instance_id)

    def instances(self) -> t.Dict[str, t.Any]:
        return self._instances

    def clear_all(self) -> None:
        self._instances.clear()


class ReferenceManager(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._references: t.Dict[str, list[t.Callable[[t.Any], None]]] = {}

    def __enter__(self) -> 'ReferenceManager':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._resolve_references()
        self._references.clear()

    def request_instant_reference(self, instance_id: str) -> t.Optional[t.Any]:
        return InstanceManager().get_instance(instance_id)

    def request_deferred_reference(self, instance_id: str, reference_setter: t.Callable[[t.Any], None]) -> None:
        if not instance_id or not reference_setter:
            return
        self._request_reference(instance_id, reference_setter)

    def _request_reference(self, instance_id: str, reference_setter: t.Callable[[t.Any], None]) -> None:
        logger.debug(f'Requesting deferred reference: {instance_id} : {reference_setter}')
        if instance_id in self._references:
            self._references[instance_id].append(reference_setter)
        else:
            self._references[instance_id] = [reference_setter]

    def _resolve_references(self) -> None:
        for instance_id, setters in self._references.items():
            instance = InstanceManager().get_instance(instance_id)
            if not instance:
                logger.error(f'Reference instance does not exist: {instance_id}')
                continue
            for setter in setters:
                logger.debug(f'Resolving reference: {instance} : {setter}')
                setter(instance)

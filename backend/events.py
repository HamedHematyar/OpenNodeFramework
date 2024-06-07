import typing as t
from abc import ABC, abstractmethod
from functools import wraps
from enum import Enum

from backend.logger import logger


class EventExecutionPhase(Enum):
    Pre = 'pre'
    Post = 'post'


def register_event(event_name, callback_type=EventExecutionPhase.Post):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if callback_type == EventExecutionPhase.Pre:
                EventManager().trigger(event_name)

            result = func(*args, **kwargs)

            if callback_type == EventExecutionPhase.Post:
                EventManager().trigger(event_name, *args, **kwargs)

            return result
        return wrapped
    return decorator


class AbstractEvent(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def register(self, callback: t.Callable) -> bool:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def deregister(self, callback: t.Callable) -> bool:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def trigger(self, callback: t.Callable) -> bool:
        raise NotImplementedError('this method is not implemented in subclass.')


class Event:
    def __init__(self):
        self._callbacks = []

    def __str__(self):
        """
        Returns a string representation of the event.
        """
        return self.__class__.__name__

    def register_callback(self, callback: t.Callable) -> bool:
        if not callable(callback):
            raise TypeError(f"callback must be a callable function : {type(callback)}")

        self._callbacks.append(callback)
        return True

    def deregister_callback(self, callback: t.Callable) -> bool:
        if not callable(callback):
            raise TypeError(f"callback must be a callable function : {type(callback)}")

        if callback not in self._callbacks:
            raise KeyError(f"callback {callback} is not registered.")

        self._callbacks.remove(callback)
        return True

    def trigger(self, *args, **kwargs) -> bool:
        for callback in self._callbacks:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.exception(e)

        return True

    def callbacks(self):
        return self._callbacks


class NodeCreated(Event):
    def __init__(self):
        super().__init__()


class NodeRemoved(Event):
    def __init__(self):
        super().__init__()


class AttributeCreated(Event):
    def __init__(self):
        super().__init__()


class AttributeRemoved(Event):
    def __init__(self):
        super().__init__()


class PortCreated(Event):
    def __init__(self):
        super().__init__()


class PortRemoved(Event):
    def __init__(self):
        super().__init__()


class GraphCreated(Event):
    def __init__(self):
        super().__init__()


class GraphRemoved(Event):
    def __init__(self):
        super().__init__()


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
            logger.debug(f"{cls.__name__} instance initialized : {instance}")

        return cls._instances[cls]


class EventManager(metaclass=SingletonMeta):
    def __init__(self):
        from backend.registry import RegisteredEvents
        self._events = {name: event() for name, event in RegisteredEvents.items()}

    def get_event(self, event_name):
        return self._events.get(event_name)

    def register_callback(self, event_name, callback: t.Callable) -> bool:
        return self._events[event_name].register_callback(callback)

    def deregister_callback(self, event_name, callback: t.Callable) -> bool:
        return self._events[event_name].deregister_callback(callback)

    def trigger(self, event_name, *args, **kwargs) -> bool:
        return self._events[event_name].trigger(*args, **kwargs)




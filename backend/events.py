import typing as t
from abc import ABC, abstractmethod
from functools import wraps
from enum import Enum

from backend.logger import logger


class EventExecutionPhase(Enum):
    Undefined = 'undefined'
    Pre = 'pre'
    Post = 'post'


def register_event(events):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            for event in [event for event in events if event.phase == EventExecutionPhase.Pre]:
                EventManager().trigger(event)

            result = func(*args, **kwargs)

            for event in [event for event in events if event.phase == EventExecutionPhase.Post]:
                EventManager().trigger(event, *args, **kwargs)

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
        self.phase = EventExecutionPhase.Undefined
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


class NodePreInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class NodePostInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class NodePreInitialized(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class NodePostInitialized(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class NodePreRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class NodePostRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class AttributePreInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class AttributePostInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class AttributePreInitialized(Event):
    def __init__(self):
        super().__init__()
        self.phase = EventExecutionPhase.Pre


class AttributePostInitialized(Event):
    def __init__(self):
        super().__init__()
        self.phase = EventExecutionPhase.Post


class AttributePreRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class AttributePostRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class PortPreInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class PortPostInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class PortPreInitialized(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class PortPostInitialized(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class PortPreRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class PortPostRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class GraphPreInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class GraphPostInstanced(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class GraphPreInitialized(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class GraphPostInitialized(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


class GraphPreRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Pre


class GraphPostRemoved(Event):
    def __init__(self):
        super().__init__()

        self.phase = EventExecutionPhase.Post


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

    def get_event(self, event):
        return self._events.get(event.__name__)

    def register_callback(self, event, callback: t.Callable) -> bool:
        return self._events[event.__name__].register_callback(callback)

    def deregister_callback(self, event, callback: t.Callable) -> bool:
        return self._events[event.__name__].deregister_callback(callback)

    def trigger(self, event, *args, **kwargs) -> bool:
        return self._events[event.__name__].trigger(*args, **kwargs)




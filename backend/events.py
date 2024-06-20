import typing as t
from abc import ABC, abstractmethod
from functools import wraps
from enum import Enum

from backend.logger import logger
from backend.meta import SingletonMeta


class EventExecutionPhase(Enum):
    Undefined = 'undefined'
    Pre = 'pre'
    Post = 'post'


def register_events_decorator(events):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            for event in [event for event in events if event.Phase == EventExecutionPhase.Pre]:
                EventManager().trigger(event, *args, **kwargs)

            result = func(*args, **kwargs)

            for event in [event for event in events if event.Phase == EventExecutionPhase.Post]:
                EventManager().trigger(event, *args, **kwargs)

            return result
        return wrapped
    return decorator


class AbstractEvent(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @abstractmethod
    def register(self, callback: t.Callable) -> bool:
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @abstractmethod
    def deregister(self, callback: t.Callable) -> bool:
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @abstractmethod
    def trigger(self, callback: t.Callable) -> bool:
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class Event:
    Phase = EventExecutionPhase.Undefined

    def __init__(self):
        self._callbacks = []

    def __str__(self):
        """
        Returns a string representation of the event.
        """
        return self.__class__.__name__

    def register_callback(self, callback: t.Callable) -> bool:
        if not callable(callback):
            raise TypeError(f'callback must be a callable function : {type(callback)}')

        self._callbacks.append(callback)
        return True

    def deregister_callback(self, callback: t.Callable) -> bool:
        if not callable(callback):
            raise TypeError(f'callback must be a callable function : {type(callback)}')

        if callback not in self._callbacks:
            raise KeyError(f'callback {callback} is not registered.')

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


class PreNodeInitialized(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostNodeInitialized(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PreNodeDeleted(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostNodeDeleted(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PreTypeInitialized(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostTypeInitialized(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PreTypeDeleted(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostTypeDeleted(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PreTypeDataChanged(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostTypeDataChanged(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PrePortInitialized(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostPortInitialized(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PrePortDeleted(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostPortDeleted(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PreGraphInitialized(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostGraphInitialized(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


class PreGraphDeleted(Event):
    Phase = EventExecutionPhase.Pre

    def __init__(self):
        super().__init__()


class PostGraphDeleted(Event):
    Phase = EventExecutionPhase.Post

    def __init__(self):
        super().__init__()


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




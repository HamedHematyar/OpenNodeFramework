import typing as t
from abc import ABC, abstractmethod
from functools import wraps
import enum

from backend.registry import register_event
from backend.logger import logger
from backend.meta import SingletonMeta


class EventExecutionPhase(enum.Enum):
    UNDEFINED = 'undefined'
    PRE = 'pre'
    POST = 'post'


def register_events_decorator(event_enums):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            event_manager = EventManager()
            events: t.Optional[t.List[Event]] = [event_manager.get_event_by_name(e.name).__class__ for e in event_enums]

            for event in (e for e in events if e.Phase == EventExecutionPhase.PRE):
                event_manager.trigger(event, *args, **kwargs)

            result = func(*args, **kwargs)

            for event in (e for e in events if e.Phase == EventExecutionPhase.POST):
                event_manager.trigger(event, *args, **kwargs)

            return result
        return wrapped
    return decorator


class AbstractEvent(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError('This method must be defined in the subclass.')

    @abstractmethod
    def register(self, callback: t.Callable) -> bool:
        raise NotImplementedError('This method must be defined in the subclass.')

    @abstractmethod
    def deregister(self, callback: t.Callable) -> bool:
        raise NotImplementedError('This method must be defined in the subclass.')

    @abstractmethod
    def trigger(self, *args, **kwargs) -> bool:
        raise NotImplementedError('This method must be defined in the subclass.')


class Event(AbstractEvent):
    Phase = EventExecutionPhase.UNDEFINED

    def __init__(self):
        self._callbacks = []

    def __str__(self) -> str:
        return self.__class__.__name__

    def register(self, callback: t.Callable) -> bool:
        if not callable(callback):
            raise TypeError(f'Callback must be a callable function, got {type(callback)}.')
        self._callbacks.append(callback)
        return True

    def deregister(self, callback: t.Callable) -> bool:
        if callback not in self._callbacks:
            raise KeyError(f'Callback {callback} is not registered.')
        self._callbacks.remove(callback)
        return True

    def trigger(self, *args, **kwargs) -> bool:
        for callback in self._callbacks:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
        return True

    def callbacks(self) -> t.List[t.Callable]:
        return self._callbacks


def create_event_class(name: str, execution_phase: EventExecutionPhase) -> t.Type[Event]:
    event_class = type(name, (Event,), {'Phase': execution_phase})

    return t.cast(t.Type[Event], event_class)


class Events(enum.Enum):
    PreNodeInitialized = enum.auto()
    PostNodeInitialized = enum.auto()
    PreNodeDeleted = enum.auto()
    PostNodeDeleted = enum.auto()
    PreTypeInitialized = enum.auto()
    PostTypeInitialized = enum.auto()
    PreTypeDeleted = enum.auto()
    PostTypeDeleted = enum.auto()
    PreTypeDataChanged = enum.auto()
    PostTypeDataChanged = enum.auto()
    PrePortInitialized = enum.auto()
    PostPortInitialized = enum.auto()
    PrePortDeleted = enum.auto()
    PostPortDeleted = enum.auto()


_event_classes = [
    (Events.PreNodeInitialized, EventExecutionPhase.PRE),
    (Events.PostNodeInitialized, EventExecutionPhase.POST),
    (Events.PreNodeDeleted, EventExecutionPhase.PRE),
    (Events.PostNodeDeleted, EventExecutionPhase.POST),
    (Events.PreTypeInitialized, EventExecutionPhase.PRE),
    (Events.PostTypeInitialized, EventExecutionPhase.POST),
    (Events.PreTypeDeleted, EventExecutionPhase.PRE),
    (Events.PostTypeDeleted, EventExecutionPhase.POST),
    (Events.PreTypeDataChanged, EventExecutionPhase.PRE),
    (Events.PostTypeDataChanged, EventExecutionPhase.POST),
    (Events.PrePortInitialized, EventExecutionPhase.PRE),
    (Events.PostPortInitialized, EventExecutionPhase.POST),
    (Events.PrePortDeleted, EventExecutionPhase.PRE),
    (Events.PostPortDeleted, EventExecutionPhase.POST)
]

for event_enum, phase in _event_classes:
    register_event(create_event_class(event_enum.name, phase))


class EventManager(metaclass=SingletonMeta):
    def __init__(self):
        from backend import registry
        event_types = registry.registered_types(registry.Category.EVENT)
        self._events = {name: event() for name, event in event_types.items()}

    def get_event(self, event: t.Type[Event]) -> t.Optional[Event]:
        return self._events.get(event.__name__)

    def get_event_by_name(self, event_name: str) -> t.Optional[Event]:
        return self._events.get(event_name)

    def register_callback(self, event: t.Type[Event], callback: t.Callable) -> bool:
        return self._events[event.__name__].register(callback)

    def deregister_callback(self, event: t.Type[Event], callback: t.Callable) -> bool:
        return self._events[event.__name__].deregister(callback)

    def trigger(self, event: t.Type[Event], *args, **kwargs) -> bool:
        return self._events[event.__name__].trigger(*args, **kwargs)
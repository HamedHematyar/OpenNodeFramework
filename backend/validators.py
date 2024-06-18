import warnings
import typing as t
from functools import wraps
from abc import ABC, abstractmethod


class AbstractValidator(ABC):

    @abstractmethod
    def validate(self, data: t.Any) -> bool:
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class BaseValidator(AbstractValidator):
    def validate(self, data: t.Any) -> bool:
        return bool(data)


def validate(validator: t.Union[t.Callable, BaseValidator]):
    def decorator(func: t.Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(validator, BaseValidator):
                validation_func = validator.validate
            elif callable(validator):
                validation_func = validator
            else:
                raise TypeError(f'validator must be a callable or an instance of {BaseValidator}.')

            if not validation_func(*args, **kwargs):
                return False

            return func(*args, **kwargs)
        return wrapper
    return decorator


def attribute_name_validator(instance, name) -> bool:
    if not isinstance(name, str):
        raise ValueError('attribute name must be a valid string.')

    return True


def port_name_validator(instance, name) -> bool:
    if not isinstance(name, str):
        raise ValueError('port name must be a valid string.')

    return True


def node_name_validator(instance, name) -> bool:
    return True


class ExampleValidator(BaseValidator):
    def validate(self, data: int) -> bool:
        return bool(data)



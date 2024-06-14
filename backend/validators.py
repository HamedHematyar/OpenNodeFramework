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


def validate(validator: t.Union[t.Callable[[t.Any], bool], BaseValidator]):
    def decorator(func: t.Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = args[0]

            if isinstance(validator, BaseValidator):
                validation_func = validator.validate
            elif callable(validator):
                validation_func = validator
            else:
                raise TypeError(f'validator must be a callable or an instance of {BaseValidator}.')

            if validation_func(data):
                raise ValueError(f'validation failed : {validation_func} : {data}')

            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_validate(data: int) -> bool:
    return bool(data)


class PositiveValidator(BaseValidator):
    def validate(self, data: int) -> bool:
        return bool(data)

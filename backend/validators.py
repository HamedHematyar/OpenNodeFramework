from typing import Any, Callable, Union
from functools import wraps
from abc import ABC, abstractmethod


class AbstractValidator(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError('This method must be defined in the subclass.')


class BaseValidator(AbstractValidator):
    def validate(self, data: Any) -> bool:
        return bool(data)


ValidatorType = Union[Callable[..., bool], BaseValidator]


def validate(validator: ValidatorType):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            if isinstance(validator, BaseValidator):
                validation_func = validator.validate
            elif callable(validator):
                validation_func = validator
            else:
                raise TypeError(f'Validator must be callable or an instance of {BaseValidator}.')

            if not validation_func(*args, **kwargs):
                return False

            return func(*args, **kwargs)

        return wrapper

    return decorator

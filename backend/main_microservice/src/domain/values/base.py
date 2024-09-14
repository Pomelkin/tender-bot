from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True, order=True)
class BaseValueObject[T](ABC):
    value: T

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self): ...

    @abstractmethod
    def as_generic_type(self) -> T: ...

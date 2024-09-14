from copy import copy
from dataclasses import dataclass, field
import abc
import uuid
from typing import Any, Iterable
from domain.events.base import BaseEvent
from domain.values.base import BaseValueObject


@dataclass
class BaseEntity(abc.ABC):
    id: uuid.UUID = field(default_factory=uuid.uuid4, kw_only=True)
    __events: list[BaseEvent] = field(default_factory=list, kw_only=True)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id

    def register_event(self, event: BaseEvent) -> None:
        self.__events.append(event)

    def pull_events(self) -> list[BaseEvent]:
        registered_events = copy(self.__events)
        self.__events.clear()
        return registered_events

    def model_dump(self) -> dict:

        def to_dict_recursive(obj: Any) -> Any:
            if isinstance(obj, BaseValueObject):
                return obj.as_generic_type()
            elif isinstance(obj, BaseEntity):
                return {
                    key: to_dict_recursive(value)
                    for key, value in obj.model_dump().items()
                }
            elif isinstance(obj, Iterable) and not isinstance(obj, str):
                return [to_dict_recursive(item) for item in obj]
            elif isinstance(obj, uuid.UUID):
                return str(obj)
            else:
                return obj

        return {
            key: to_dict_recursive(value) for key, value in self.__dict__.items() if key != "_BaseEntity__events"
                                                                                     and key != "discarded"
        }

from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    title: str
    text: str

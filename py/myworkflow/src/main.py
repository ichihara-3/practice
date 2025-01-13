from dataclasses import dataclass
from typing import Callable, Generic, Protocol, TypeVar

T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    result: T
    exc: None | Exception


class Handler(Protocol):
    def __call__(self, *args, **kwargs) -> Result: ...


class Task:
    def __init__(self, handler: Handler):
        self._handler: Handler = handler

    def run(self, *args, **kwargs)->Result:
        return self._handler(*args, **kwargs)

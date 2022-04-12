from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Any

T = TypeVar("T")


@dataclass
class BaseProcessor(Generic[T], ABC):
    """
    A parser that can extract and process data from an external service. This parser is intended for tasks that:
      1. Can cache all the data required upon the app's start (in the 'store' instance), so it only parses once.
      2. Cannot use I/O libraries based in asyncio
    """
    url: str
    store: Any

    def __post_init__(self):
        self.store = self.parse()

    @abstractmethod
    def get(self, *_) -> T:
        ...

    def parse(self):
        """Extracts and parses data from the given URL. This method must be overridden for use case (1)"""
        return None


@dataclass
class AsyncBaseProcessor(Generic[T], ABC):
    """A parser that can asynchronously extract and process data from an external service"""
    url: str  # https://www.bls.gov/web/laus/lauhsthl.htm

    async def async_teardown(self):
        """Utility method that gets called in the asyncio loop upon the app's shutdown"""
        pass

    @abstractmethod
    async def get(self, *_) -> T:
        ...

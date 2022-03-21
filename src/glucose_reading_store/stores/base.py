"""
The protocol implementation of the glucose reading store.
This represents the interface used by the other stores.

"""
from abc import ABCMeta, abstractmethod
from types import TracebackType
from typing import Iterator, Type, Union
from uuid import UUID

from ..models import GlucoseReading


class AbstractGlucoseReadingStore(metaclass=ABCMeta):
    """
    An abstract representation of a glucose reading store.

    This should raise a `NoSuchReading` error if an attempt is made to
    fetch or modify a reading that does not exist, and a pydantic
    `ValidationError` if the reading fails to validate. If a reading
    with the same reading UUID is added twice, a `DuplicateReading`
    error should be raised.

    If the store must be used as a context manager, it should raise a
    `NotInContext` error if access is attempted outside the context.

    """

    @abstractmethod
    def add_reading(self, reading: GlucoseReading):
        """
        Create a glucose reading, raising a `DuplicateReading` exception
        if the error reading already exists in the store.

        """

    @abstractmethod
    def update_reading(self, reading: GlucoseReading):
        """
        Update a glucose reading, raising a `NoSuchReading` exception if
        the error does not exist in the store.

        """

    @abstractmethod
    def get_reading(self, reading_uuid: Union[int, str, UUID]) -> GlucoseReading:
        """
        Fetch a reading from its UUID, raising a `NoSuchReading` exception
        if the error does not exist in the store.

        If there is a failure creating a `GlucoseReading` from the store entry,
        bubble up the pydantic `ValidationError`.

        """

    @abstractmethod
    def delete_reading(self, reading_uuid: Union[int, str, UUID]):
        """
        Delete a reading using its UUID, raising a `NoSuchReading` exception
        if the error does not exist in the store.

        """

    @abstractmethod
    def iterate_readings(self) -> Iterator[GlucoseReading]:
        """Iterate through all the readings in the store."""

    @abstractmethod
    def __enter__(self):
        """Enter the reading store's context."""

    @abstractmethod
    def __exit__(
        self, exc_type: Type[Exception], exc_value: Exception, traceback: TracebackType
    ):
        """Exit the reading store's context."""

    def __iter__(self) -> Iterator[GlucoseReading]:
        yield from self.iterate_readings()

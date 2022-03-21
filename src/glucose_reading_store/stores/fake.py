"""
A fake implementation of the glucose reading store built
on top of a dictionary.

This should be used for unit tests.

"""
from types import TracebackType
from typing import Iterator, Type, Union
from uuid import UUID

from .base import AbstractGlucoseReadingStore
from ..common import parse_uuid
from ..exceptions import DuplicateReading, NoSuchReading
from ..models import GlucoseReading


class FakeGlucoseReadingStore(AbstractGlucoseReadingStore):
    """
    A fake glucose reading store built on top of a Python dictionary.

    """

    def __init__(self):
        self._readings = {}

    def add_reading(self, reading: GlucoseReading):
        reading_uuid = reading.reading_uuid
        if reading_uuid in self._readings:
            raise DuplicateReading(repr(reading_uuid))

        self._readings[reading_uuid] = reading

    def update_reading(self, reading: GlucoseReading):
        reading_uuid = reading.reading_uuid
        if reading_uuid not in self._readings:
            raise NoSuchReading(repr(reading_uuid))

        self._readings[reading_uuid] = reading

    def get_reading(self, reading_uuid: Union[int, str, UUID]) -> GlucoseReading:
        reading_uuid = parse_uuid(reading_uuid)
        try:
            return self._readings[reading_uuid]
        except KeyError as err:
            raise NoSuchReading(repr(reading_uuid)) from err

    def delete_reading(self, reading_uuid: Union[int, str, UUID]):
        reading_uuid = parse_uuid(reading_uuid)
        try:
            del self._readings[reading_uuid]
        except KeyError as err:
            raise NoSuchReading(reading_uuid) from err

    def iterate_readings(self) -> Iterator[GlucoseReading]:
        yield from self._readings.values()

    def __enter__(self):
        pass

    def __exit__(
        self, exc_type: Type[Exception], exc_value: Exception, traceback: TracebackType
    ):
        pass

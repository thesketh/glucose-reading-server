"""
A concreate implementation of the glucose reading store built
on top of SQLAlchemy

"""

from types import TracebackType
from typing import Iterator, Optional, Type, Union
from uuid import UUID

from sqlalchemy import Column, DateTime, String
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound

from .base import AbstractGlucoseReadingStore
from ..common import parse_uuid
from ..exceptions import DuplicateReading, NoSuchReading, NotInContext
from ..models import GlucoseReading


Base = declarative_base()


class GlucoseReadingEntry(Base):
    """The database model for the glucose reading pydantic model."""

    __tablename__ = "readings"
    # Ideally UUIDs would be BigIntegers but SQLite doesn't support
    # 128 bit integers.
    reading_uuid = Column(String(length=36), primary_key=True)
    patient_uuid = Column(String(length=36))
    value = Column(String)
    units = Column(String)
    recorded_at = Column(DateTime)

    @classmethod
    def from_reading(cls, reading: GlucoseReading):
        """Create a glucose reading database entry from a reading."""
        return cls(
            reading_uuid=str(reading.reading_uuid),
            patient_uuid=str(reading.patient_uuid),
            value=str(reading.value),
            units=reading.units,
            recorded_at=reading.recorded_at,
        )

    def to_reading(self) -> GlucoseReading:
        """Create a glucose reading from a database entry."""
        return GlucoseReading(
            patient_uuid=self.patient_uuid,
            reading_uuid=self.reading_uuid,
            value=self.value,
            units=self.units,
            recorded_at=self.recorded_at,
        )


class SQLAlchemyGlucoseReadingStore(AbstractGlucoseReadingStore):
    """
    A glucose reading store built on top of SQLAlchemy.

    """

    def __init__(self, engine: Engine):
        Base.metadata.create_all(engine)
        self._session_factory = sessionmaker(engine)
        self.__session: Optional[Session] = None

    @property
    def _session(self) -> Session:
        """The session, if the store is being used as a context."""
        if self.__session is None:
            raise NotInContext("This reading store must be used as a context manager.")
        return self.__session

    def _get_current_entry(self, reading_uuid: str) -> GlucoseReadingEntry:
        """Return the current entry for a given UUID (as a string)."""
        try:
            return (
                self._session.query(GlucoseReadingEntry)
                .filter(GlucoseReadingEntry.reading_uuid == reading_uuid)
                .one()
            )
        except NoResultFound as err:
            raise NoSuchReading(UUID(reading_uuid)) from err

    def add_reading(self, reading: GlucoseReading):
        entry = GlucoseReadingEntry.from_reading(reading)
        self._session.add(entry)
        try:
            self._session.flush()
        except IntegrityError as err:
            raise DuplicateReading(reading.reading_uuid) from err

    def update_reading(self, reading: GlucoseReading):
        new_entry = GlucoseReadingEntry.from_reading(reading)
        current_entry = self._get_current_entry(new_entry.reading_uuid)

        current_entry.patient_uuid = new_entry.patient_uuid
        current_entry.value = new_entry.value
        current_entry.units = new_entry.units
        current_entry.recorded_at = new_entry.recorded_at

        self._session.flush()

    def get_reading(self, reading_uuid: Union[str, int, UUID]) -> GlucoseReading:
        entry = self._get_current_entry(str(parse_uuid(reading_uuid)))
        return entry.to_reading()

    def delete_reading(self, reading_uuid: Union[int, str, UUID]):
        entry = self._get_current_entry(str(parse_uuid(reading_uuid)))
        self._session.delete(entry)
        self._session.flush()

    def iterate_readings(self) -> Iterator[GlucoseReading]:
        entry: GlucoseReadingEntry
        for entry in self._session.query(GlucoseReadingEntry):
            yield entry.to_reading()

    def __enter__(self):
        self.__session = self._session_factory()
        self.__session.__enter__()
        return self

    def __exit__(
        self, exc_type: Type[Exception], exc_value: Exception, traceback: TracebackType
    ):
        return_value = self.__session.__exit__(exc_type, exc_value, traceback)  # type: ignore
        self.__session = None
        return return_value

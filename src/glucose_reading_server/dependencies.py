"""Dependencies required by the API."""
from contextvars import ContextVar

from sqlalchemy import create_engine

from glucose_reading_store.stores import (
    AbstractGlucoseReadingStore,
    FakeGlucoseReadingStore,
    SQLAlchemyGlucoseReadingStore,
)

reading_store: ContextVar[AbstractGlucoseReadingStore] = ContextVar("reading_store")


def set_reading_store_engine(connection_string: str):
    """Set the reading store's engine from a connection string."""
    engine = create_engine(connection_string)
    reading_store.set(SQLAlchemyGlucoseReadingStore(engine))


def set_test_reading_store():
    """Set the reading store to use a test store."""
    reading_store.set(FakeGlucoseReadingStore())

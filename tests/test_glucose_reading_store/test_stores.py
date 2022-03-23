"""
Tests for glucose reading stores.

"""
# pylint: disable=redefined-outer-name
from pathlib import Path
import datetime as dt
from tempfile import TemporaryDirectory
from typing import Iterator
from uuid import uuid4

import pytest
from sqlalchemy import create_engine

from glucose_reading_store.exceptions import (
    DuplicateReading,
    NoSuchReading,
    NotInContext,
)
from glucose_reading_store.models import GlucoseReading
from glucose_reading_store.stores import (
    AbstractGlucoseReadingStore,
    SQLAlchemyGlucoseReadingStore,
    FakeGlucoseReadingStore,
)


@pytest.fixture
def reading() -> Iterator[GlucoseReading]:
    """A sample glucose reading."""
    yield GlucoseReading(
        patient_uuid=uuid4(),
        value="1.1",
        units="mmol/L",
        recorded_at=dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc),
    )


@pytest.fixture
def fake_store() -> Iterator[FakeGlucoseReadingStore]:
    """A fixture providing a fake store."""
    yield FakeGlucoseReadingStore()


@pytest.fixture
def sqlite_store() -> Iterator[SQLAlchemyGlucoseReadingStore]:
    """A fixture providing a store using SQLite."""
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir, "some_db.db")
        engine = create_engine(f"sqlite:///{path}")
        yield SQLAlchemyGlucoseReadingStore(engine)


@pytest.mark.parametrize("store_fixture", ["sqlite_store", "fake_store"])
def test_store_add_get(
    request: pytest.FixtureRequest, store_fixture: str, reading: GlucoseReading
):
    """Test that readings can be fetched and inserted."""
    store: AbstractGlucoseReadingStore = request.getfixturevalue(store_fixture)

    with store:
        store.add_reading(reading)
        assert store.get_reading(reading.reading_uuid) == reading


@pytest.mark.parametrize("store_fixture", ["sqlite_store", "fake_store"])
def test_store_iterator(
    request: pytest.FixtureRequest, store_fixture: str, reading: GlucoseReading
):
    """Test that readings can be inserted and iterated through."""
    store: AbstractGlucoseReadingStore = request.getfixturevalue(store_fixture)

    with store:
        store.add_reading(reading)
        assert next(iter(store)) == reading


@pytest.mark.parametrize("store_fixture", ["sqlite_store", "fake_store"])
def test_store_delete(
    request: pytest.FixtureRequest, store_fixture: str, reading: GlucoseReading
):
    """Test that readings can be deleted as expeceted."""
    store: AbstractGlucoseReadingStore = request.getfixturevalue(store_fixture)

    with store:
        store.add_reading(reading)
        store.delete_reading(reading.reading_uuid)
        with pytest.raises(NoSuchReading):
            store.get_reading(reading.reading_uuid)


@pytest.mark.parametrize("store_fixture", ["sqlite_store", "fake_store"])
def test_modify_reading(
    request: pytest.FixtureRequest, store_fixture: str, reading: GlucoseReading
):
    """Test that readings can be inserted and iterated through."""
    store: AbstractGlucoseReadingStore = request.getfixturevalue(store_fixture)

    with store:
        store.add_reading(reading)

        new_reading = GlucoseReading(
            reading_uuid=reading.reading_uuid,
            patient_uuid=reading.patient_uuid,
            value="23.0",
            units="mg/dL",
            recorded_at=dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc),
        )

        store.update_reading(new_reading)
        assert store.get_reading(reading.reading_uuid) == new_reading


@pytest.mark.parametrize("store_fixture", ["sqlite_store", "fake_store"])
def test_duplicate_reading_raises(
    request: pytest.FixtureRequest, store_fixture: str, reading: GlucoseReading
):
    """
    Test that `DuplicateReading` are raised when an attempt is made to add a
    duplicate reading.

    """
    store: AbstractGlucoseReadingStore = request.getfixturevalue(store_fixture)

    with store:
        store.add_reading(reading)

        with pytest.raises(DuplicateReading):
            store.add_reading(reading)


@pytest.mark.parametrize("store_fixture", ["sqlite_store", "fake_store"])
def test_update_missing_reading_raises(
    request: pytest.FixtureRequest, store_fixture: str, reading: GlucoseReading
):
    """
    Test that `NoSuchReading` errors are raised when an attempt is made to
    update a nonexistent reading.

    """
    store: AbstractGlucoseReadingStore = request.getfixturevalue(store_fixture)

    with store:
        with pytest.raises(NoSuchReading):
            store.update_reading(reading)


@pytest.mark.parametrize("store_fixture", ["sqlite_store", "fake_store"])
def test_delete_missing_reading_raises(
    request: pytest.FixtureRequest, store_fixture: str, reading: GlucoseReading
):
    """
    Test that `NoSuchReading` errors are raised when an attempt is made to
    delete a nonexistent reading.

    """
    store: AbstractGlucoseReadingStore = request.getfixturevalue(store_fixture)

    with store:
        with pytest.raises(NoSuchReading):
            store.delete_reading(reading.reading_uuid)


def test_sqlite_store_requires_context(
    sqlite_store: SQLAlchemyGlucoseReadingStore, reading: GlucoseReading
):
    """Test that the SQLite store raises an error if used outside a context."""
    with pytest.raises(NotInContext):
        sqlite_store.add_reading(reading)

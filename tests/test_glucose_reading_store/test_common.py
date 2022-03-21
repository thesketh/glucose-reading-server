"""
Tests for common code (e.g. UUID parsing).

"""
from typing import Union
from uuid import UUID

import pytest

from glucose_reading_store.common import parse_uuid


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        [
            "37f8fd2a-6f9c-42aa-9495-18f806793897",
            UUID("37f8fd2a-6f9c-42aa-9495-18f806793897"),
        ],
        [123, UUID("00000000-0000-0000-0000-00000000007b")],
        [
            UUID("39d687a7-54a3-43c1-b2e3-c63060e495f6"),
            UUID("39d687a7-54a3-43c1-b2e3-c63060e495f6"),
        ],
    ],
)
def test_parse_uuid(value: Union[UUID, int, str], expected: UUID):
    """Test the happy path for UUID parsing."""
    assert parse_uuid(value) == expected


def test_uuid_invalid_value():
    """Test the unhappy path for UUID parsing with invalid values."""
    with pytest.raises(ValueError):
        parse_uuid("some-non-uuid-string")

    with pytest.raises(ValueError):
        parse_uuid(-1)

    with pytest.raises(ValueError):
        parse_uuid(2**128 + 1)


def test_uuid_invalid_type():
    """Test the unhappy path for UUID parsing with invalid types."""
    with pytest.raises(TypeError):
        parse_uuid(None)

    with pytest.raises(TypeError):
        parse_uuid(5.0)

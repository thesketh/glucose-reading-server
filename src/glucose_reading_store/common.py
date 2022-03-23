"""
Service layer code which might be required by multiple components.

"""
import datetime as dt
from typing import Union
from uuid import UUID


def parse_uuid(uuid_value: Union[int, str, UUID]) -> UUID:
    """Parse a UUID from a string or int, if necessary."""
    if isinstance(uuid_value, UUID):
        return uuid_value

    if isinstance(uuid_value, str):
        return UUID(uuid_value)

    if isinstance(uuid_value, int):
        return UUID(int=uuid_value)

    raise TypeError(f"UUID must be UUID, string or int, got {type(uuid_value)}")


def format_as_tz_aware_iso(datetime: dt.datetime) -> str:
    """
    Format a datetime as TZ-aware ISO-8601. This will strip microseconds
    from the timestamp.

    """
    if datetime.tzinfo is None:
        datetime = datetime.astimezone(dt.timezone.utc)
    return datetime.replace(microsecond=0).isoformat()

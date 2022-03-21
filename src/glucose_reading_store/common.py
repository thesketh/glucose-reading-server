"""
Service layer code which might be required by multiple components.

"""
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

"""Exceptions raised by interactions with the reading store."""


class DuplicateReading(ValueError):
    """Raised when an attempt is made to log a duplicate reading."""


class NoSuchReading(KeyError):
    """Raised when a reading does not exist."""


class NotInContext(ValueError):
    """Raised when context managers are accessed outside the context."""

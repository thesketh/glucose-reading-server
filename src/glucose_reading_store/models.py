"""Pydantic models used by the glucose reading store."""
import datetime as dt
from decimal import Decimal
from typing import Literal, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator  # pylint: disable=no-name-in-module

from .common import parse_uuid


class GlucoseReading(BaseModel):  # pylint: disable=too-few-public-methods
    """A glucose reading from a patient."""

    reading_uuid: UUID = Field(default_factory=uuid4)
    """A unique identifier representing the reading itself."""
    patient_uuid: UUID
    """A unique identifier representing the patient."""
    value: Decimal
    """
    The quantity of the glucose concentration in the patient's blood at the time
    of the reading.

    """
    units: Literal["mmol/L", "mg/dL"]
    """
    The units of the glucose concentration in the patient's blood at the time
    of the reading.

    """
    recorded_at: dt.datetime
    """The time the reading was recorded."""

    @validator("patient_uuid", "reading_uuid", pre=True, allow_reuse=True)
    def parse_uuid(  # pylint: disable=no-self-use,no-self-argument
        cls, uuid_value: Union[int, str, UUID]
    ) -> Optional[UUID]:
        """Parse a UUID from a string or int, if necessary."""
        # For non-required 'reading_uuid'.
        if uuid_value is None:  # pragma: no cover
            return None

        return parse_uuid(uuid_value)

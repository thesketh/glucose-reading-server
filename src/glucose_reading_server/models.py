"""Reading/update request models for the API."""
from decimal import Decimal
from typing import Literal, Optional
import datetime as dt
from uuid import UUID

from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module


class ReadingCreateRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """A request to log a glucose reading."""

    patient_uuid: UUID
    value: Decimal
    unit: Literal["mmol/L", "mg/dL"]
    recorded_at: dt.datetime

    @validator("recorded_at")
    def assert_tz_aware(  # pylint: disable=no-self-use,no-self-argument
        cls, timestamp: dt.datetime
    ) -> dt.datetime:
        """Make sure recorded time is TZ-aware."""
        if timestamp.tzinfo is None:
            raise ValueError("`recorded_at` must be TZ-aware.")
        return timestamp


class ReadingUpdateRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """A request to update a glucose reading."""

    patient_uuid: Optional[UUID]
    value: Optional[Decimal]
    unit: Optional[Literal["mmol/L", "mg/dL"]]
    recorded_at: Optional[dt.datetime]

    @validator("recorded_at")
    def assert_tz_aware(  # pylint: disable=no-self-use,no-self-argument
        cls, timestamp: Optional[dt.datetime]
    ) -> Optional[dt.datetime]:
        """Make sure recorded time is TZ-aware (if provided)."""
        if timestamp is None:
            return None

        if timestamp.tzinfo is None:
            raise ValueError("`recorded_at` must be TZ-aware.")
        return timestamp

"""
App routing for the glucose reading server.

"""
from typing import List
from uuid import UUID

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import ValidationError

from glucose_reading_store.models import GlucoseReading
from glucose_reading_store.exceptions import NoSuchReading, DuplicateReading

from .dependencies import reading_store
from .models import ReadingCreateRequest, ReadingUpdateRequest


APP = FastAPI()


@APP.exception_handler(RequestValidationError)
async def handle_inbound_validation_failure(
    _: Request, exc: RequestValidationError
) -> PlainTextResponse:
    """
    Switch inbound validation (i.e. request body parsing) to return
    400 upon error instead of 422.

    """
    return PlainTextResponse(status_code=400, content=exc.json())


@APP.exception_handler(ValidationError)
async def handle_validation_failure(
    _: Request, exc: ValidationError
) -> PlainTextResponse:
    """Return status 400 for model validation failures."""
    return PlainTextResponse(status_code=400, content=exc.json())


@APP.exception_handler(NoSuchReading)
async def handle_no_such_reading(_: Request, exc: NoSuchReading) -> JSONResponse:
    """Return status 404 for missing readings."""
    return JSONResponse(status_code=404, content=repr(exc))


@APP.exception_handler(DuplicateReading)
async def handle_duplicate_reading(_: Request, exc: DuplicateReading) -> JSONResponse:
    """Return status 400 for duplicate readings."""
    return JSONResponse(status_code=400, content=repr(exc))


@APP.get("/v1/reading", status_code=200)
async def list_readings() -> List[GlucoseReading]:
    """List all glucose readings."""
    store = reading_store.get()
    with store:
        return list(store)


@APP.post("/v1/reading", status_code=201)
async def add_reading(create_request: ReadingCreateRequest) -> GlucoseReading:
    """Process a reading create request, returning the reading."""
    store = reading_store.get()
    with store:
        reading = GlucoseReading(
            patient_uuid=create_request.patient_uuid,
            value=create_request.value,
            unit=create_request.unit,
            recorded_at=create_request.recorded_at,
        )
        store.add_reading(reading)
        return reading


@APP.get("/v1/reading/{reading_uuid}")
async def get_reading(reading_uuid: UUID) -> GlucoseReading:
    """Get a glucose reading from its UUID."""
    store = reading_store.get()
    with store:
        return store.get_reading(reading_uuid)


@APP.put("/v1/reading/{reading_uuid}", status_code=204)
async def update_reading(
    reading_uuid: UUID, update_request: ReadingUpdateRequest, response: Response
) -> Response:
    """Process a reading update request, returning the reading."""
    store = reading_store.get()
    with store:
        current_reading = store.get_reading(reading_uuid)

        reading = GlucoseReading(
            reading_uuid=current_reading.reading_uuid,
            patient_uuid=update_request.patient_uuid or current_reading.patient_uuid,
            value=update_request.value or current_reading.value,
            unit=update_request.unit or current_reading.unit,
            recorded_at=update_request.recorded_at or current_reading.recorded_at,
        )
        store.update_reading(reading)

    response.status_code = 204
    response.body = b""
    return response


@APP.delete("/v1/reading/{reading_uuid}", status_code=204)
async def delete_reading(reading_uuid: UUID, response: Response) -> Response:
    """Process a reading update request, returning the reading."""
    store = reading_store.get()

    with store:
        store.delete_reading(reading_uuid)

    response.status_code = 204
    response.body = b""
    return response

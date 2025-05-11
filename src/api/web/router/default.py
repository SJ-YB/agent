import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router: APIRouter = APIRouter()


class Status(BaseModel):
    status: str = "OK"


@router.get("/", response_model=Status)
@router.get("/healthz", response_model=Status)
@router.get("/readyz", response_model=Status)
@router.get("/livez", response_model=Status)
async def health() -> Status:
    return Status()


@router.get("/startupz", response_model=Status)
async def startup() -> Status:
    instances: list[Any] = []

    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(obj.ready()) for obj in instances]

    if all(t.result() for t in tasks):
        return Status()

    raise HTTPException(status_code=500, detail="Dependencies are not ready.")

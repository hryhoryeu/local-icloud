from typing import Annotated

from sqlalchemy import orm as so
from fastapi import APIRouter, Depends

from database import get_db

internal_router = APIRouter(prefix="/test", tags=["Test"])


@internal_router.get("/db", description="db var preloaded")
async def test(db: Annotated[so.Session, Depends(get_db)]):
    import ipdb

    ipdb.set_trace()

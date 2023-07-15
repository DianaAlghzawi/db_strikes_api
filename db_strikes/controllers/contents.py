from uuid import UUID

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from db_strikes.controllers.models.contents import Contents, PatchContents
from db_strikes.infra.db.engine import engine
from db_strikes.repositories import contents

contents_router = APIRouter(
    prefix='/contents',
    tags=['Contents']
)


@contents_router.post('')
async def insert(content: Contents) -> JSONResponse:
    with engine.begin() as conn:
        return JSONResponse(content=jsonable_encoder(contents.new(conn, content.body, content.status)), status_code=status.HTTP_201_CREATED)


@contents_router.get('/{id}')
async def get_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        return JSONResponse(content=jsonable_encoder(contents.get_by_id(conn, id)), status_code=status.HTTP_200_OK)


@contents_router.delete('/{id}')
async def delete(id: UUID) -> Response:
    with engine.begin() as conn:
        contents.delete(conn, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@contents_router.patch('/{id}')
async def update(id: UUID, patch_content: PatchContents) -> JSONResponse:
    with engine.begin() as conn:
        content = contents.get_by_id(conn, id)
        content.body = patch_content.body if patch_content.body else content.body
        content.status = patch_content.status if patch_content.status else content.status
        return JSONResponse(content=jsonable_encoder(contents.update(conn, id, content)), status_code=status.HTTP_200_OK)

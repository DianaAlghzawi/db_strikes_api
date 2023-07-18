from uuid import UUID

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from db_strikes.controllers.models.contents import Content, PatchContents
from db_strikes.services import contents

contents_router = APIRouter(
    prefix='/contents',
    tags=['Contents']
)


@contents_router.post('')
async def insert(content: Content) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(contents.new(content.body, content.status, content.author_id)),
                        status_code=status.HTTP_201_CREATED)


@contents_router.get('/{id}')
async def get_by_id(id: UUID) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(contents.get_by_id(id)), status_code=status.HTTP_200_OK)


@contents_router.delete('/{id}')
async def delete(id: UUID) -> Response:
    contents.delete(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@contents_router.patch('/{id}')
async def update(id: UUID, patch_content: PatchContents) -> JSONResponse:
    content = contents.get_by_id(id)
    content.body = patch_content.body if patch_content.body else content.body
    content.status = patch_content.status if patch_content.status else content.status
    return JSONResponse(content=jsonable_encoder(contents.update(id, content)), status_code=status.HTTP_200_OK)

from uuid import UUID

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from db_strikes.controllers.models.contents import Contents, PatchContents
from db_strikes.services import contents

contents_router = APIRouter(
    prefix='/contents',
    tags=['Contents']
)


@contents_router.post('')
async def insert(content: Contents) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(contents.new_content(content.body, content.status)), status_code=status.HTTP_201_CREATED)


@contents_router.get('/{id}')
async def get_by_id(id: UUID) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(contents.get_content_by_id(id)), status_code=status.HTTP_200_OK)


@contents_router.delete('/{id}')
async def delete(id: UUID) -> Response:
    contents.delete_content(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@contents_router.patch('/{id}')
async def update(id: UUID, patch_content: PatchContents) -> JSONResponse:
    content = contents.get_content_by_id(id)
    content.body = patch_content.body if patch_content.body else content.body
    content.status = patch_content.status if patch_content.status else content.status
    return JSONResponse(content=jsonable_encoder(contents.update_content(id, content)), status_code=status.HTTP_200_OK)

from uuid import UUID

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from db_strikes.controllers.models.authors import Author, PatchAuthor
from db_strikes.services import authors

authors_router = APIRouter(
    prefix='/authors',
    tags=['Authors']
)


@authors_router.post('')
async def insert(auther: Author) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(authors.new_author(auther.bio)), status_code=status.HTTP_201_CREATED)


@authors_router.get('/{id}')
async def get_by_id(id: UUID) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(authors.get_author_by_id(id)), status_code=status.HTTP_200_OK)


@authors_router.delete('/{id}')
async def delete(id: UUID) -> Response:
    authors.delete_author(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@authors_router.patch('/{id}')
async def update(id: UUID, patch_author: PatchAuthor) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(authors.update_author(id, patch_author.bio)), status_code=status.HTTP_200_OK)

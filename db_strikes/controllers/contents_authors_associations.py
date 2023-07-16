
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from db_strikes.services.strikes.add_author_to_content import NewAuthorToContent
from db_strikes.services.strikes.delete_author_from_content import \
    DeleteAuthorFromContent
from db_strikes.services.strikes.remove_links_from_body import RemoveLinksFromBody

contents_authors_router = APIRouter(
    prefix='/contents',
    tags=['contents_authers']
)


@contents_authors_router.post('/{content_id}/authors/{author_id}')
async def add_author_to_content(content_id: UUID, author_id: UUID) -> JSONResponse:
    content_author = NewAuthorToContent(content_id, author_id)
    content_auther = content_author.add_author_to_content()
    return JSONResponse(content=jsonable_encoder(content_auther), status_code=status.HTTP_201_CREATED)


@contents_authors_router.delete('/{content_id}/authors/{author_id}')
async def delete_author_from_content(content_id: UUID, author_id: UUID) -> Response:
    DeleteAuthorFromContent(content_id, author_id).delete_author_from_content()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@contents_authors_router.patch('/remove_links/{content_id}')
def remove_links_from_body(id: UUID) -> JSONResponse:
    return JSONResponse(content=jsonable_encoder(RemoveLinksFromBody(id).remove_links_from_body()), status_code=status.HTTP_200_OK)

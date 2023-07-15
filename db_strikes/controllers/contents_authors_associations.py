
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from db_strikes.controllers.models.contents_authors_associations import ContentAuthor
from db_strikes.infra.db.engine import engine
from db_strikes.repositories import contents_authors_associations
from db_strikes.repositories.strikes import add_author_to_content


contents_authors_router = APIRouter(
    prefix='/contents',
    tags=['contents_authers']
)


@contents_authors_router.post("/{content_id}/authors/{author_id}")
async def add_author_to_content(content_id: UUID, author_id: UUID) -> JSONResponse:
    # Call the repository function to add the author to the content
    content = add_author_to_content(content_id, author_id)

    return JSONResponse(
        content={"message": "Author added to content successfully"},
        status_code=status.HTTP_200_OK,
    )


# @contents_authors_router.post('')
# async def insert(content_auther: ContentAuthor) -> JSONResponse:
#     with engine.begin() as conn:
#         return JSONResponse(content=jsonable_encoder(contents_authors_associations.new(conn, content_auther.content_id, content_auther.author_id)), status_code=status.HTTP_201_CREATED)


# @contents_authors_router.get('/{id}')
# async def get_by_id(id: UUID) -> JSONResponse:
#     with engine.connect() as conn:
#         return JSONResponse(content=jsonable_encoder(authors.get_by_id(conn, id)), status_code=status.HTTP_200_OK)


# @contents_authors_router.delete('/{id}')
# async def delete(cont: UUID) -> Response:
#     with engine.begin() as conn:
#         authors.delete(conn, id)
#         return Response(status_code=status.HTTP_204_NO_CONTENT)


# @contents_authors_router.patch('/{id}')
# async def update(id: UUID, patch_author: PatchAuthor) -> JSONResponse:
#     with engine.begin() as conn:
#         return JSONResponse(content=jsonable_encoder(authors.update(conn, id, patch_author.bio)), status_code=status.HTTP_200_OK)

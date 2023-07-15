from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from db_strikes.controllers.authors import authors_router
from db_strikes.controllers.contents import contents_router
from db_strikes.controllers.contents_authors_associations import contents_authors_router
from db_strikes.exception import ModelNotFoundException

app = FastAPI()

app.include_router(authors_router)
app.include_router(contents_router)
app.include_router(contents_authors_router)


@app.exception_handler(ModelNotFoundException)
async def unicorn_not_found_exception_handler(request: Request, exc: ModelNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exc.content},
    )

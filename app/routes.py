"""indengsvc API

"""
import logging
import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse

from app.service.tokens import update_employees_data
from app.service.users import get_user, get_users

logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": "indengsvc API",
        "description": "Manipulate with indengsvc Employees and Teams",
    },
]

DESCRIPTION = """
    # Response Codes
    ## HTTP Status Codes
    Our API returns standard HTTP success or error status codes as listed below.

    Code | Title | Description
    -|-|-
    200 | Success | The request was successful

    # API Status Codes
    In addition to the regular HTTP response codes the API will include an api_status
    code with further details as listed below.

    Code | Description
    -|-
    1001 | Method Not Allowed


    ## Alternative documentation formats
    * [Swagger](/docs)
    * [ReDoc](/redoc)
"""

# Create an application instance
api_app = FastAPI(
    openapi_tags=tags_metadata,
)

security = HTTPBasic()


@api_app.exception_handler(Exception)
async def exception_handler(request: Request, e: Exception):
    unique_event_id = secrets.token_hex(8)
    logger.exception(f"Unhandled exception (unique_event_id={unique_event_id})")
    return JSONResponse(
        {
            "exception": f"{e.__class__.__name__}: {str(e)}",
            "unique_event_id": unique_event_id,
        },
        status_code=500,
    )


def custom_openapi():
    if api_app.openapi_schema:
        return api_app.openapi_schema
    openapi_schema = get_openapi(
        title="Indeng Inc. API",
        version="0.0.1",
        description="\n".join([line.lstrip() for line in DESCRIPTION.split("\n")]),
        routes=api_app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    api_app.openapi_schema = openapi_schema
    return api_app.openapi_schema


api_app.openapi = custom_openapi

api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# -- API Definition starts here ---------------------------------------------


@api_app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@api_app.get("/users/me")
def read_current_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}


@api_app.get(
    "/v1/employees",
    tags=["Employees"],
    status_code=200,
    summary="Update Employees data from legacy API in `users` table",
)
async def update_employees_data_v1():
    update_employees_data()

    return (
        "Employees data from legacy API "
        "has been successfully updated in `users` table"
    )


@api_app.get(
    "/v1/users",
    tags=["Users"],
    status_code=200,
    summary="Get all users",
)
async def get_users_all_v1():
    return get_users()


@api_app.get(
    "/v1/users/{user_id}",
    tags=["Users"],
    status_code=200,
    summary="Get user by user_id",
)
async def get_user_by_id_v1(user_id: str):
    return get_user(user_id)

"""indengsvc API

This file defines the routes for the indengsvc API.
It includes endpoints for manipulating Indengsvc Users/Employees and Teams.
The API requires authentication using HTTP Basic authentication.
The API documentation is available in Swagger and ReDoc formats.

The API endpoints are as follows:
- GET /v1/employees: Update Employees data from a legacy API in the `users` table.
- GET /v1/users: Get all users.
- GET /v1/users/{user_id}: Get a specific user by user_id.
"""

import logging
import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse

from app.service.employees import update_employees_data
from app.service.users import get_user, get_users

# Set up logging
logger = logging.getLogger(__name__)

# Load credentials from environment variables
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

if not USERNAME:
    raise RuntimeError("USERNAME is not specified!")

if not PASSWORD:
    raise RuntimeError("PASSWORD is not specified!")

# Set up API documentation metadata
tags_metadata = [
    {
        "name": "indengsvc API",
        "description": "Manipulate with Indengsvc Users/Employees and Teams",
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
api_app = FastAPI(openapi_tags=tags_metadata)

security = HTTPBasic()


# Set up exception handling
@api_app.exception_handler(Exception)
async def exception_handler(request: Request, e: Exception):
    """Handles exceptions that occur during request processing."""
    unique_event_id = secrets.token_hex(8)
    logger.exception(f"Unhandled exception (unique_event_id={unique_event_id})")
    return JSONResponse(
        {
            "exception": f"{e.__class__.__name__}: {str(e)}",
            "unique_event_id": unique_event_id,
        },
        status_code=500,
    )


# Set up custom OpenAPI documentation
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

# Set up CORS middleware
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["Authorization"],
    allow_credentials=True,
)


# Define authentication function
def authenticate_user(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    """Authenticates a user using basic authentication credentials."""
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# -- API Definition starts here ---------------------------------------------


# Define API endpoints with input validation and authentication


@api_app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@api_app.get(
    "/v1/employees",
    tags=["Employees"],
    status_code=200,
    summary="Update Employees data from legacy API in `users` table",
)
async def update_employees_data_v1(username: str = Depends(authenticate_user)):
    """Update Employees data from legacy API in `users` table."""
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
async def get_users_all_v1(username: str = Depends(authenticate_user)):
    """Get all users."""
    return get_users()


@api_app.get(
    "/v1/users/{user_id}",
    tags=["Users"],
    status_code=200,
    summary="Get user by user_id",
)
async def get_user_by_id_v1(user_id: str, username: str = Depends(authenticate_user)):
    """Get user by user_id."""
    # Validate and sanitize user_id
    if not user_id.isnumeric():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user_id: {user_id}",
        )
    return get_user(user_id)

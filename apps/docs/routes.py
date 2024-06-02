<<<<<<< HEAD
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html


router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="My API",
        oauth2_redirect_url="/docs/oauth2-redirect",
    )

=======
from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html


router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="My API",
        oauth2_redirect_url="/docs/oauth2-redirect",
    )

>>>>>>> b9c9b7ce59051f80f8dd40d88d8dc081e9a64c07

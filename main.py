import os

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from apps.core import routes as core_router
from apps.docs import routes as docs_router
from apps.auth.middlewares import AuthMiddleware
from apps.docs.custom_openai import custom_openapi
from apps.ikesaki import routes as ikesaki_router

load_dotenv()


def init_db(instance: FastAPI) -> None:
    register_tortoise(
        instance,
        db_url=os.getenv("DATABASE_URL"),
        modules={"models": ["apps.core.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


def create_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(AuthMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=[
            "DELETE",
            "GET",
            "OPTIONS",
            "PATCH",
            "POST",
            "PUT",
        ],
        allow_headers=["*"]
    )

    application.include_router(docs_router.router, tags=['ikesaki', 'core'])
    application.include_router(ikesaki_router.router, prefix="/ikesaki",
                               tags=['ikesaki'])
    application.include_router(core_router.router, prefix="/core",
                               tags=['core'])

    return application


app = create_application()

app.openapi = lambda: custom_openapi(app)


@app.on_event('startup')
async def startup_event():
    init_db(app)

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from auth.base_config import fastapi_users, auth_backend
from auth.schemas import UserRead, UserCreate
from products.router import products_router, categories_router
from products.logger import products_formatter, products_handler

from redis import asyncio as aioredis


main_handler = logging.FileHandler(filename='logs/main.log')
main_handler.setFormatter(products_formatter)

main_logger = logging.Logger(name='main_logger')
main_logger.addHandler(main_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url('redis://localhost')
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield


app = FastAPI(lifespan=lifespan, title='Some Store')

main_router = APIRouter()
main_router.include_router(products_router)
main_router.include_router(categories_router)

main_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

main_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

main_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

main_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


main_router.include_router(
    fastapi_users.get_users_router(user_schema=UserRead, user_update_schema=UserCreate, requires_verification=True),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(main_router)


@app.get('/')
async def home_page():
    try:
        return {
            'status': 'success',
            'data': None,
            'details': 'Добро пожаловать на сайт Some Store!'
        }
    except Exception:
        main_logger.error('Some home_page error')
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Внутренняя ошибка сервера'
        })


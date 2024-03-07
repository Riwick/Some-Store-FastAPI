import logging

from fastapi import FastAPI, APIRouter, HTTPException

from products.router import products_handler, products_router, products_formatter, categories_router

main_handler = logging.FileHandler(filename='logs/main.log')
main_handler.setFormatter(products_formatter)

main_logger = logging.Logger(name='main_logger')
main_logger.addHandler(main_handler)

app = FastAPI()

main_router = APIRouter()
main_router.include_router(products_router)
main_router.include_router(categories_router)

app.include_router(main_router)


@app.get('/')
async def home_page():
    try:
        return {
            'status': 'success',
            'data': None,
            'details': 'Самый лучший магазин в мире!!!'
        }
    except Exception:
        main_logger.error('Some home_page error')
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Внутренняя ошибка сервера'
        })


logging.basicConfig(handlers=(products_handler, main_handler), level=logging.ERROR)

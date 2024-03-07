import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from database import get_async_session
from products.models import Product, Category
from products.categories_schemas import CategoryCreateUpdate
from products.products_schemas import ProductCreateUpdate

products_router = APIRouter(
    prefix='/products',
    tags=['products']
)

products_formatter = logging.Formatter('%(levelname)s:%(name)s-%(asctime)s-%(message)s')
products_handler = logging.FileHandler('logs/products.log')
products_handler.setFormatter(products_formatter)

products_logger = logging.Logger(name='products_logger')
products_logger.addHandler(products_handler)


@products_router.get('/')
async def get_many_products(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Product).limit(10)
        result = await session.execute(query)
        if result:
            return {
                'status': 'success',
                'data': result.mappings().all(),
                'details': None
            }
        else:
            return {
                'status': 'not_found',
                'data': None,
                'details': 'Ни найдено ни одного предложения, проверьте параметры поиска'
            }
    except Exception:
        products_logger.error(f'Some get_products error')
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Внутренняя ошибка сервера'
        })


@products_router.get('/{product_id}')
async def get_product_id(product_id: int, session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    try:
        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)
        result2 = await session.execute(query)
        if result2.mappings().all():
            return {
                'status': 'success',
                'data': result.mappings().all(),
                'details': None
            }
        else:
            return {
                'status': 'not_found',
                'data': None,
                'details': 'Продукт не найден'
            }
    except Exception:
        products_logger.error(f'Some get_products error')
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Внутренняя ошибка сервера'
        })


@products_router.post('/')
async def add_product(product_data: ProductCreateUpdate, session: AsyncSession = Depends(get_async_session),
                      user=Depends(current_user)):
    if user:
        try:
            stmt = insert(Product).values(**product_data.dict())
            await session.execute(stmt)
            await session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': 'Продукт добавлен!'
            }
        except Exception:
            products_logger.error(f'Some add_product error')
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'details': 'Внутренняя ошибка сервера'
            })


@products_router.delete('/{product_id}')
async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session),
                         user=Depends(current_user)):
    if user:
        try:
            query = select(Product).where(Product.id == product_id)
            result = await session.execute(query)
            if result.mappings().first():
                stmt = delete(Product).where(Product.id == product_id)
                await session.execute(stmt)
                await session.commit()
                return {
                    'status': 'success',
                    'data': None,
                    'details': 'Продукт удален!'
                }
            else:
                return {
                    'status': 'not_found',
                    'data': None,
                    'details': 'Продукт не найден'
                }
        except Exception:
            products_logger.error(f'Some delete_product error')
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'details': 'Внутренняя ошибка сервера'
            })


@products_router.put('/{product_id}')
async def update_product(product_id: int, product_data: ProductCreateUpdate,
                         session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    if user:
        try:
            query = select(Product).where(Product.id == product_id)
            result = await session.execute(query)

            if result.mappings().first():
                stmt = update(Product).where(Product.id == product_id).values(**product_data.dict())
                await session.execute(stmt)
                await session.commit()
                return {
                    'status': 'success',
                    'data': None,
                    'details': 'Продукт обновлен!'
                }
            else:
                return {
                    'status': 'not_found',
                    'data': None,
                    'details': 'Продукт не найден'
                }
        except Exception:
            products_logger.error('Some update_product error')
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'details': 'Внутренняя ошибка сервера'
            })

categories_router = APIRouter(
    prefix='/categories',
    tags=['categories']
)


@categories_router.get('/')
async def get_categories(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Category).limit(10)
        result = await session.execute(query)
        result2 = await session.execute(query)
        if result2.mappings().all():
            return {
                'status': 'success',
                'data': result.mappings().all(),
                'details': None
            }
        else:
            return {
                'status': 'not_found',
                'data': None,
                'details': 'Не найдено ни одной категории, проверьте параметры поиска'
            }
    except Exception:
        products_logger.error(f'Some get_categories error')
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Внутренняя ошибка сервера'
        })


@categories_router.post('/')
async def add_category(category_data: CategoryCreateUpdate, session: AsyncSession = Depends(get_async_session),
                       user=Depends(current_user)):
    if user:
        try:
            stmt = insert(Category).values(**category_data.dict())
            await session.execute(stmt)
            await session.commit()
            return {
                'status': 'success',
                'data': None,
                'details': 'Категория добавлена!'
            }
        except Exception:
            products_logger.error(f'Some add_category error')
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'details': 'Внутренняя ошибка сервера'
            })


@categories_router.delete('/{category_id}')
async def delete_category(category_id: int, session: AsyncSession = Depends(get_async_session),
                          user=Depends(current_user)):
    if user:
        try:
            query = select(Category).where(Category.id == category_id)
            result = await session.execute(query)

            if result.mappings().all():
                stmt = delete(Category).where(Category.id == category_id)
                await session.execute(stmt)
                await session.commit()

                return {
                    'status': 'success',
                    'data': None,
                    'details': 'Категория удалена!'
                }
            else:
                return {
                    'status': 'not_found',
                    'data': None,
                    'details': 'Категория не найдена'
                }
        except Exception:
            products_logger.error('Some delete_category error')
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'details': 'Внутренняя ошибка сервера'
            })


@categories_router.put('/{category_id}')
async def update_category(category_id: int, category_data: CategoryCreateUpdate,
                          session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    if user:
        try:
            query = select(Category).where(Category.id == category_id)
            result = await session.execute(query)

            if result.mappings().all():
                stmt = update(Category).where(Category.id == category_id).values(**category_data.dict())
                await session.execute(stmt)
                await session.commit()

                return {
                    'status': 'success',
                    'data': None,
                    'details': 'Категория обновлена!'
                }
            else:
                return {
                    'status': 'not_found',
                    'data': None,
                    'details': 'Категория не найдена'
                }
        except Exception:
            products_logger.error('Some update_category error')
            raise HTTPException(status_code=500, detail={
                'status': 'error',
                'data': None,
                'details': 'Внутренняя ошибка сервера'
            })

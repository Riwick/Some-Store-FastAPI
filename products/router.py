from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from fastapi_filter import FilterDepends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import current_user
from database import get_async_session
from products.filters import ProductFilter, CategoryFilter
from products.logger import products_logger
from products.models import Product, Category
from products.categories_schemas import CategoryCreateUpdate
from products.products_schemas import ProductCreateUpdate

products_router = APIRouter(
    prefix='/products',
    tags=['products']
)

base_per_page = 10


@products_router.get('/')
# @cache(expire=60, namespace='get_many_products')
async def get_many_products(per_page: int = base_per_page, page: int = 0, session: AsyncSession = Depends(get_async_session),
                            product_filter: ProductFilter = FilterDepends(ProductFilter)):
    if per_page > 30:
        raise HTTPException(status_code=400, detail={
            'status': 'error',
            'data': None,
            'details': 'Количество объектов на странице должно быть меньше 30'
        })
    try:
        query = product_filter.filter(select(Product).limit(per_page).offset(page * per_page))
        query = product_filter.sort(query)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None,
            'page': page,
            'page_size': per_page,
        }
    except Exception:
        products_logger.error(f'Some get_products error')
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': 'Внутренняя ошибка сервера'
        })


@products_router.get('/{product_id}')
@cache(expire=3600, namespace='get_product_id')
async def get_product_id(product_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Product).where(Product.id == product_id)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None
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
# @cache(expire=3600, namespace='get_categories')
async def get_categories(page_size: int = base_per_page, page: int = 0, session: AsyncSession = Depends(get_async_session),
                         category_filter: CategoryFilter = FilterDepends(CategoryFilter)):
    if page_size > 30:
        raise HTTPException(status_code=400, detail={
            'status': 'error',
            'data': None,
            'details': 'Количество объектов на странице должно быть меньше 30'
        })
    try:
        query = select(Category).limit(page_size).offset(page * page_size)
        query = category_filter.sort(query)
        result = await session.execute(query)
        return {
            'status': 'success',
            'data': result.mappings().all(),
            'details': None,
            'page': page,
            'page_size': page_size
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

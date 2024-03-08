from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from products.models import Product, Category


class ProductFilter(Filter):
    title: Optional[str] = None
    price: Optional[int] = None
    order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = Product


class CategoryFilter(Filter):
    title: Optional[str] = None
    order_by: Optional[list[str]] = None

    class Constants(Filter.Constants):
        model = Category

from sqlalchemy import Table, Column, Integer, String, DECIMAL, ForeignKey, Float

from database import Base, metadata


class Category(Base):
    __tablename__ = 'category'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)


class Product(Base):
    __tablename__ = 'product'
    metadata = metadata

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(ForeignKey('category.id'))

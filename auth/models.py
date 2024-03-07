from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, Table
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, metadata

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('register_time', TIMESTAMP, default=datetime.utcnow),
    Column('is_active', Boolean, default=False, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=True, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String, nullable=False)
    username = Column('username', String, nullable=False)
    registered_at = Column('register_time', TIMESTAMP, default=datetime.utcnow)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

from typing import TYPE_CHECKING
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy import Enum
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from datetime import datetime

from utils.ERoles import Roles
from models.base import Base
from models.orders import Orders_Products

if TYPE_CHECKING:
    from .orders import Orders


class Catalog(Base):
    __tablename__ = "catalog"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    product_description: Mapped[str] = mapped_column(String(250))
    product_cost: Mapped[str] = mapped_column(String(10))
    product_cost_d: Mapped[str] = mapped_column(String(10))

    date_create: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    date_update: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                  onupdate=func.now())

    orders: Mapped["Orders"] = relationship(secondary="orders_products", back_populates="product")

    def __str__(self) -> str:
        return f"Catalog(id = {self.id!r})"

    def __repr__(self) -> str:
        # return super().__repr__()
        return str(self)
